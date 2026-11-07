import logging
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
from app.core.config import settings

logger = logging.getLogger(__name__)

# Common agricultural dictionary translations for instant caching
AGRICULTURAL_TRANSLATION_CACHE: Dict[Tuple[str, str, str], str] = {
    ("Tomato Early Blight", "en", "mr"): "टोमॅटोचा लवकर येणारा करपा (Early Blight)",
    ("Tomato Early Blight", "en", "hi"): "टमाटर का अगेती झुलसा (Early Blight)",
    ("Tomato Late Blight", "en", "mr"): "टोमॅटोचा उशिरा येणारा करपा (Late Blight)",
    ("Tomato Late Blight", "en", "hi"): "टमाटर का पछेती झुलसा (Late Blight)",
    ("Rice Blast", "en", "mr"): "भाताचा करपा रोग (Rice Blast)",
    ("Rice Blast", "en", "hi"): "धान का झोंका रोग (Rice Blast)",
    ("Wheat Rust", "en", "mr"): "गव्हाचा तांबेरा रोग (Wheat Rust)",
    ("Wheat Rust", "en", "hi"): "गेहूं का गेरुआ रोग (Wheat Rust)",
    ("Cotton Bacterial Blight", "en", "mr"): "कपाशीचा जिवाणूजन्य करपा (काळी काठी)",
    ("Cotton Bacterial Blight", "en", "hi"): "कपास का जीवाणु झुलसा रोग",
    ("Healthy Crop", "en", "mr"): "निरोगी पीक",
    ("Healthy Crop", "en", "hi"): "स्वस्थ फसल",
}


class TranslationProvider(ABC):
    @abstractmethod
    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        pass


class BhashiniTranslationProvider(TranslationProvider):
    """Bhashini ULCA / Dhruva NMT API Provider."""

    def __init__(self):
        self.api_key = settings.BHASHINI_API_KEY
        self.user_id = settings.BHASHINI_USER_ID
        self.pipeline_url = settings.BHASHINI_PIPELINE_URL

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not self.api_key or self.api_key == "your-bhashini-api-key":
            return text

        try:
            payload = {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": source_lang,
                                "targetLanguage": target_lang
                            }
                        }
                    }
                ],
                "inputData": {
                    "input": [{"source": text}]
                }
            }
            headers = {
                "Authorization": self.api_key,
                "Content-Type": "application/json"
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(self.pipeline_url, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    output_text = data["pipelineResponse"][0]["output"][0]["target"]
                    return output_text
        except Exception as e:
            logger.warning(f"Bhashini translation API request failed: {e}")

        return text


class IndicTrans2Provider(TranslationProvider):
    """Local / Mock IndicTrans2 inference provider."""

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        # Check cache
        if (text, source_lang, target_lang) in AGRICULTURAL_TRANSLATION_CACHE:
            return AGRICULTURAL_TRANSLATION_CACHE[(text, source_lang, target_lang)]
        return text


class TranslationService:
    def __init__(self):
        self.bhashini_provider = BhashiniTranslationProvider()
        self.indic_provider = IndicTrans2Provider()
        self._memory_cache: Dict[Tuple[str, str, str], str] = dict(AGRICULTURAL_TRANSLATION_CACHE)

    def detect_language(self, text: str) -> str:
        """Heuristic Devanagari character detection."""
        devanagari_count = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        if devanagari_count > len(text) * 0.2:
            # Check for characteristic Marathi characters/words
            marathi_markers = ["आहे", "नाही", "शेतकरी", "करावे", "पिक", "झाले", "आणि"]
            if any(marker in text for marker in marathi_markers):
                return "mr"
            return "hi"
        return "en"

    async def translate_text(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        """Translate text with caching and fallback."""
        if not text or not text.strip():
            return ""

        if not source_lang:
            source_lang = self.detect_language(text)

        if source_lang == target_lang:
            return text

        cache_key = (text.strip(), source_lang, target_lang)
        if cache_key in self._memory_cache:
            return self._memory_cache[cache_key]

        # 1. Try Bhashini
        if settings.BHASHINI_API_KEY:
            translated = await self.bhashini_provider.translate(text, source_lang, target_lang)
            if translated != text:
                self._memory_cache[cache_key] = translated
                return translated

        # 2. Try IndicTrans2 / local fallback
        translated = await self.indic_provider.translate(text, source_lang, target_lang)
        self._memory_cache[cache_key] = translated
        return translated
