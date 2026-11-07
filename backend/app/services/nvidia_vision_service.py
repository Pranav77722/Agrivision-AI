import base64
import json
import logging
import io
import re
from typing import Optional, Dict, Any, List
import httpx
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)


def extract_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Extract first complete JSON object from text using bracket balancing."""
    if not text:
        return None
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    start = cleaned.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(cleaned)):
        c = cleaned[i]
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if not in_string:
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    candidate = cleaned[start : i + 1]
                    try:
                        return json.loads(candidate)
                    except Exception:
                        pass
    return None


class NvidiaVisionService:
    """NVIDIA NIM Multimodal Vision Service for Plant Foliar Disease Diagnosis.

    Uses high-speed multimodal vision reasoning (nvidia/nemotron-3-nano-omni-30b-a3b-reasoning)
    to inspect leaf morphology, lesions, chlorosis, and foliar health.
    Rotates automatically through all available NVIDIA NIM API keys.
    """

    @classmethod
    async def analyze_leaf(
        cls,
        image_bytes: bytes,
        crop_hint: str = "Unknown",
        cloud_image_url: Optional[str] = None,
        language: str = "en"
    ) -> Optional[Dict[str, Any]]:
        """Analyze a leaf image using NVIDIA NIM Vision API with comprehensive diagnostic prompt."""
        # Consolidate all available user keys with deduplication
        all_keys = [settings.NVIDIA_API_KEY] + [k for k in settings.NVIDIA_BACKUP_KEYS if k]
        seen = set()
        api_keys: List[str] = [k for k in all_keys if k and not (k in seen or seen.add(k))]

        # Prepare direct base64 data URI payload (preferred over URL to avoid external download blocks)
        try:
            img = Image.open(io.BytesIO(image_bytes))
            # Downscale large mobile camera photos to ~768px for fast transfer (<150KB)
            if max(img.size) > 768:
                img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            img.convert("RGB").save(buf, format="JPEG", quality=85)
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            image_target = f"data:image/jpeg;base64,{b64}"
        except Exception as e:
            logger.error(f"Failed to encode image for NVIDIA NIM: {e}")
            if cloud_image_url and cloud_image_url.startswith("http"):
                image_target = cloud_image_url
            else:
                return None

        hint_crop = crop_hint if crop_hint and crop_hint != "Unknown" else "crop"

        prompt = f"""You are an elite plant pathologist, agronomist, and foliar disease specialist.
Examine this crop leaf photo with rigorous scientific diagnostic standards. The crop indicated is '{hint_crop}'.

CRITICAL INSTRUCTIONS:
1. Examine the visual evidence on the leaf surface (leaf blade, margins, venation, spots, lesions, chlorosis, necrosis, rust, powdery mildew, or clean healthy tissue).
2. NEVER copy a fixed disease template or assume any specific disease unless clear visual evidence exists in this specific image.
3. If the leaf is healthy and clean, diagnose it as '<Crop> Healthy Foliage' with is_healthy: true, severity_level: 'Healthy', diseased_area_percent: 0.0, healthy_area_percent: 100.0, urgency_window: 'None'.
4. If diseased, identify the exact disease, causal pathogen, visual symptoms, organic treatments, chemical treatments, dosage, and attention regions.

Return a complete, valid JSON object matching this schema:
{{
  "crop_type": "<Identified crop name, e.g. Tomato, Potato, Pepper, Maize, Rice, Cotton, Wheat, Grape, Apple, Citrus>",
  "predicted_disease": "<Specific diagnosed disease condition, or '<Crop> Healthy Foliage' if disease-free>",
  "pathogen": "<Causal organism if diseased (e.g. Fungus, Bacteria, Virus, Oomycete), or 'None' if healthy>",
  "is_healthy": <true if healthy foliage, false if diseased>,
  "confidence": <confidence score between 0.70 and 0.99>,
  "severity_level": "<Healthy, Mild, Moderate, or Severe>",
  "diseased_area_percent": <estimated percentage of leaf surface covered by lesions, 0.0 if healthy>,
  "healthy_area_percent": <estimated percentage of healthy green tissue, 100.0 if healthy>,
  "urgency_window": "<e.g. None if healthy, Within 24-48 Hours, Within 3-5 Days>",
  "symptoms": [
    "<Visual symptom 1: lesion shape, color, pattern, or healthy leaf features>",
    "<Visual symptom 2: chlorosis, halos, leaf texture>",
    "<Visual symptom 3: progression or defoliation>"
  ],
  "organic_control": [
    "<Specific bio-fungicide or botanical spray with dosage per liter>",
    "<Organic cultural or biological remedy>"
  ],
  "chemical_control": [
    "<Recommended chemical active molecule with dosage per liter>",
    "<Protective or systemic fungicide/bactericide option>"
  ],
  "cultural_practices": [
    "<Sanitation, pruning, or irrigation recommendation>",
    "<Plant spacing and canopy aeration recommendation>"
  ],
  "safety_measures": [
    "<Required PPE during spraying>",
    "<Pre-harvest interval (PHI)>"
  ],
  "dosage": "<Recommended dosage summary, e.g. 2.0 - 2.5 g/L of water>",
  "spray_interval_days": <recommended days between sprays, e.g. 7 or 10>,
  "focus_description": "<Clinical visual summary of the identified leaf lesions or healthy tissue>",
  "attention_regions": [
    {{"label": "<Specific diagnostic leaf area 1>", "score": 0.92}},
    {{"label": "<Specific diagnostic leaf area 2>", "score": 0.85}}
  ]
}}

Output ONLY valid JSON without markdown fences or additional conversational text."""

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
                    "max_tokens": 4096,
                    "reasoning_budget": 512,
                    "temperature": 0.15
                }

                async with httpx.AsyncClient(timeout=25.0) as client:
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

                    parsed = extract_json_object(content)
                    if parsed:
                        parsed["ai_reasoning"] = reasoning[:300] if reasoning else ""

                        # Standardize disease name and healthy status
                        detected_crop_str = str(parsed.get("crop_type") or crop_hint or "Crop").strip().capitalize()
                        if detected_crop_str.lower() in ["unknown", "crop", ""]:
                            detected_crop_str = crop_hint.capitalize() if crop_hint != "Unknown" else "Crop"
                        parsed["crop_type"] = detected_crop_str

                        raw_disease = str(parsed.get("predicted_disease") or "").strip()
                        is_healthy = bool(parsed.get("is_healthy", False)) or raw_disease.lower() in [
                            "healthy", "none", "not applicable", "n/a", "no disease", "", "healthy foliage"
                        ] or str(parsed.get("severity_level", "")).lower() == "healthy"

                        if is_healthy:
                            parsed["is_healthy"] = True
                            parsed["predicted_disease"] = f"{detected_crop_str} Healthy Foliage"
                            parsed["severity_level"] = "Healthy"
                            parsed["diseased_area_percent"] = 0.0
                            parsed["healthy_area_percent"] = 100.0
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
                        logger.warning(f"NVIDIA NIM returned 200 but could not parse JSON: {content[:100]}")
                else:
                    logger.warning(f"NVIDIA NIM returned status {resp.status_code} with key {key[:10]}...: {resp.text[:120]}")

            except Exception as e:
                logger.warning(f"NVIDIA NIM API call failed with key {key[:10]}...: {e}")

        logger.info("NVIDIA NIM Vision API unavailable or timed out; falling back to local Agronomic CV ensemble.")
        return None
