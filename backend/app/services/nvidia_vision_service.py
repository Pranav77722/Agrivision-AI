import base64
import json
import logging
import io
import re
from typing import Optional, Dict, Any
import httpx
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)


class NvidiaVisionService:
    """NVIDIA NIM Multimodal Vision Service for Plant Foliar Disease Diagnosis.

    Uses high-speed multimodal vision reasoning (nvidia/nemotron-3-nano-omni-30b-a3b-reasoning)
    to inspect leaf morphology, lesions, chlorosis, and foliar health.
    """

    @classmethod
    async def analyze_leaf(
        cls,
        image_bytes: bytes,
        crop_hint: str = "Unknown",
        cloud_image_url: Optional[str] = None,
        language: str = "en"
    ) -> Optional[Dict[str, Any]]:
        """Analyze a leaf image using NVIDIA NIM Vision API."""
        api_keys = [settings.NVIDIA_API_KEY] + [k for k in settings.NVIDIA_BACKUP_KEYS if k != settings.NVIDIA_API_KEY]

        # Prepare image payload: prefer Cloudinary public URL, fallback to base64 data URI
        if cloud_image_url and cloud_image_url.startswith("http"):
            image_target = cloud_image_url
        else:
            try:
                # Resize if image is huge to speed up upload
                img = Image.open(io.BytesIO(image_bytes))
                img.thumbnail((768, 768))
                buf = io.BytesIO()
                img.convert("RGB").save(buf, format="JPEG", quality=85)
                b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                image_target = f"data:image/jpeg;base64,{b64}"
            except Exception as e:
                logger.error(f"Failed to encode image for NVIDIA NIM: {e}")
                return None

        prompt = (
            f"You are an expert plant pathologist and agronomist. "
            f"Analyze this plant leaf photo carefully. The farmer indicated the crop might be '{crop_hint}'. "
            f"Determine: "
            f"1. The exact crop/plant species (e.g. Tomato, Potato, Corn/Maize, Rice, Cotton, Wheat, Pepper, Apple, Grape). "
            f"2. Whether the leaf is Healthy or has a disease (e.g. Early Blight, Late Blight, Leaf Spot, Powdery Mildew, Rust, Mosaic Virus, Bacterial Blight). "
            f"3. Confidence score between 0.70 and 0.99. "
            f"4. Severity level (Healthy, Mild, Moderate, or Severe). "
            f"5. Visible symptoms description. "
            f"6. Recommended organic/biological treatment. "
            f"7. Recommended chemical treatment (if diseased, otherwise 'Not applicable'). "
            f"Respond ONLY with a valid JSON object matching this schema: "
            f'{{"crop_type": "Tomato", "predicted_disease": "Tomato Early Blight", "is_healthy": false, '
            f'"confidence": 0.92, "severity_level": "Moderate", "symptoms": "...", "organic_treatment": "...", "chemical_treatment": "..."}}'
        )

        for key in api_keys:
            if not key:
                continue
            try:
                headers = {
                    "Authorization": f"Bearer {key}",
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": settings.NVIDIA_MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": image_target}}
                            ]
                        }
                    ],
                    "max_tokens": 700,
                    "reasoning_budget": 160,
                    "temperature": 0.1
                }

                async with httpx.AsyncClient(timeout=settings.NVIDIA_TIMEOUT_SECONDS) as client:
                    resp = await client.post(
                        settings.NVIDIA_API_URL,
                        headers=headers,
                        json=payload
                    )

                if resp.status_code == 200:
                    data = resp.json()
                    choice = data.get("choices", [{}])[0]
                    message = choice.get("message", {})
                    content = message.get("content") or ""
                    reasoning = message.get("reasoning_content") or ""

                    # Extract JSON object from content
                    json_match = re.search(r"\{.*\}", content, re.DOTALL)
                    if json_match:
                        parsed = json.loads(json_match.group(0))
                        parsed["ai_reasoning"] = reasoning[:300] if reasoning else ""

                        # Standardize disease name and healthy status
                        detected_crop_str = str(parsed.get("crop_type") or crop_hint or "Plant").strip().capitalize()
                        if detected_crop_str.lower() == "unknown":
                            detected_crop_str = crop_hint.capitalize() if crop_hint != "Unknown" else "Plant"
                        parsed["crop_type"] = detected_crop_str

                        raw_disease = str(parsed.get("predicted_disease") or "").strip()
                        is_healthy = parsed.get("is_healthy", False) or raw_disease.lower() in [
                            "healthy", "none", "not applicable", "n/a", "no disease", ""
                        ] or parsed.get("severity_level", "").lower() == "healthy"

                        if is_healthy:
                            parsed["is_healthy"] = True
                            parsed["predicted_disease"] = f"{detected_crop_str} Healthy"
                            parsed["severity_level"] = "Healthy"
                            if not parsed.get("confidence") or parsed.get("confidence") < 0.8:
                                parsed["confidence"] = 0.95
                        else:
                            parsed["is_healthy"] = False
                            # Ensure crop prefix if not already present
                            if not raw_disease.lower().startswith(detected_crop_str.lower()):
                                parsed["predicted_disease"] = f"{detected_crop_str} {raw_disease}"
                            else:
                                parsed["predicted_disease"] = raw_disease

                        logger.info(f"NVIDIA NIM Vision standardized: {parsed.get('predicted_disease')} (conf: {parsed.get('confidence')})")
                        return parsed
                    else:
                        logger.warning(f"NVIDIA NIM returned 200 but could not parse JSON from content: {content[:100]}")
                else:
                    logger.warning(f"NVIDIA NIM returned status {resp.status_code}: {resp.text[:120]}")

            except Exception as e:
                logger.warning(f"NVIDIA NIM API call failed with key {key[:10]}...: {e}")

        logger.info("NVIDIA NIM Vision API unavailable or timed out; falling back to local Agronomic CV ensemble.")
        return None
