import logging
import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are 'Agrivision AI+ Krishi Mitra', an expert agricultural AI assistant designed specifically for Indian farmers.
Your goal is to provide practical, scientifically sound, and safe agricultural advice regarding:
1. Crop disease diagnosis and pest management
2. Soil health, irrigation scheduling, and fertilizer management (NPK ratios)
3. Weather-based farming decisions and crop calendar advice
4. Government agricultural schemes (PM-KISAN, PMFBY, etc.)

Safety Guardrails:
- When recommending any synthetic chemical pesticide, always state the standard safe dosage (per liter of water).
- ALWAYS advise the farmer to wear protective gloves, a mask, and goggles during spraying.
- Advise against spraying during windy conditions or immediately before rainfall.
- Recommend integrated pest management (IPM) combining organic, biological, and cultural controls.

Respond directly in the user's selected language: {language}.
Keep your advice clear, encouraging, practical, and formatted with bullet points for readability.
"""


class AssistantService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.gemini_key = settings.GEMINI_API_KEY
        self.openai_key = settings.OPENAI_API_KEY

    async def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        language: str = "en",
        farmer_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate context-aware agricultural response via LLM or curated expert engine."""
        lang_names = {"en": "English", "mr": "Marathi", "hi": "Hindi"}
        lang_label = lang_names.get(language, "English")

        context_str = ""
        if farmer_context:
            context_str = f"\nFarmer Context: State={farmer_context.get('state')}, District={farmer_context.get('district')}, Primary Crops={farmer_context.get('primary_crops')}, Soil={farmer_context.get('soil_type')}."

        system_instruction = SYSTEM_PROMPT.format(language=lang_label) + context_str

        # 1. Try Google Gemini API if key is present
        if self.gemini_key and self.gemini_key != "your-gemini-api-key":
            try:
                reply = await self._call_gemini(user_message, conversation_history, system_instruction)
                if reply:
                    return reply
            except Exception as e:
                logger.error(f"Gemini API invocation error: {e}")

        # 2. Try OpenAI API if key is present
        if self.openai_key and self.openai_key != "your-openai-api-key":
            try:
                reply = await self._call_openai(user_message, conversation_history, system_instruction)
                if reply:
                    return reply
            except Exception as e:
                logger.error(f"OpenAI API invocation error: {e}")

        # 3. Rule-based Agricultural Expert Engine Fallback
        return self._generate_expert_fallback(user_message, language, farmer_context)

    async def _call_gemini(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]],
        system_instruction: str
    ) -> Optional[str]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        
        contents = []
        if conversation_history:
            for msg in conversation_history[-6:]:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        contents.append({"role": "user", "parts": [{"text": f"Instruction: {system_instruction}\n\nUser Question: {user_message}"}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 800,
            }
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
        return None

    async def _call_openai(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]],
        system_instruction: str
    ) -> Optional[str]:
        url = "https://api.openai.com/v1/chat/completions"
        messages = [{"role": "system", "content": system_instruction}]
        if conversation_history:
            for msg in conversation_history[-6:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 800
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        return None

    def _generate_expert_fallback(
        self,
        user_message: str,
        language: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        msg_lower = user_message.lower()

        if language == "mr":
            if "रोग" in user_message or "करपा" in user_message or "डाग" in user_message:
                return (
                    "**कृषी सल्ला (रोग व्यवस्थापन):**\n"
                    "• पानांवरील डाग किंवा करपा नियंत्रणासाठी **मॅन्कोझेब ७५% WP (Mancozeb)** २.५ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारणी करावी.\n"
                    "• बुरशीचा प्रादुर्भाव जास्त असल्यास **अझोक्सिस्ट्रोबिन** किंवा **रिडोमिल** १.५ ते २ ग्रॅम प्रति लिटर वापरावे.\n"
                    "• जैविक नियंत्रणासाठी ५% निंबोळी अर्क (NSKE) किंवा ट्रायकोडर्मा फवारावे.\n"
                    "⚠️ **सावधगिरी:** फवारणी करताना तोंडाला मास्क व हातमोजे वापरा. वाऱ्याच्या उलट दिशेने फवारणी करू नका."
                )
            elif "खत" in user_message or "युरिया" in user_message:
                return (
                    "**संतुलित खत व्यवस्थापन सल्ला:**\n"
                    "• माती परीक्षणाच्या आधारेच खतांची मात्रा निश्चित करा.\n"
                    "• नत्र, स्फुरद आणि पालाश (NPK) चा समतोल ठेवा. अति युरियामुळे पिकावर कीड-रोगांचा प्रादुर्भाव वाढतो.\n"
                    "• फुलधारणेच्या व फळधारणेच्या काळात १९:१९:१९ किंवा ००:५२:३४ विद्राव्य खतांची फवारणी फायदेशीर ठरते."
                )
            return (
                "**अॅग्रीव्हिजन AI+ कृषी मित्र:**\n"
                f"नमस्कार शेतकरी बंधू! तुमच्या '{user_message}' या प्रश्नावर आम्ही तज्ज्ञांचा सल्ला तयार केला आहे.\n"
                "• तुमच्या पिकाच्या सुरक्षेसाठी नियमित निरीक्षण ठेवा.\n"
                "• रोगट भाग आढळल्यास शेतातून काढून नष्ट करा.\n"
                "• सिंचन योग्य प्रमाणात द्या आणि हवामानाचा अंदाज घेऊनच फवारणीचे नियोजन करा."
            )
        elif language == "hi":
            if "रोग" in user_message or "धब्बा" in user_message or "झुलसा" in user_message:
                return (
                    "**कृषि मित्र सलाह (रोग नियंत्रण):**\n"
                    "• पत्तियों पर धब्बों या झुलसा रोग के लिए **मैनकोजेब 75% WP** 2.5 ग्राम प्रति लीटर पानी में मिलाकर स्प्रे करें।\n"
                    "• अत्यधिक प्रकोप की स्थिति में **मेटालैक्सिल + मैनकोजेब (रिडोमिल)** 2 ग्राम प्रति लीटर छिड़कें।\n"
                    "• 5% नीम के बीज का अर्क (NSKE) जैविक नियंत्रण के रूप में उपयोग करें।\n"
                    "⚠️ **सुरक्षा निर्देश:** छिड़काव के समय मास्क और दस्ताने पहनें। हवा की विपरीत दिशा में छिड़काव न करें।"
                )
            return (
                "**एग्रीविजन AI+ कृषि मित्र:**\n"
                "नमस्ते किसान भाई! फसल की अच्छी बढ़वार के लिए नियमित देखभाल और संतुलित पोषण आवश्यक है।\n"
                "• रोगग्रस्त पौधों को तुरंत खेत से हटाकर नष्ट करें।\n"
                "• सिंचाई और कीटनाशक छिड़काव मौसम के पूर्वानुमान के अनुसार ही करें।"
            )

        # Default English
        return (
            "**Agrivision AI+ Crop Advisory:**\n"
            "• For leaf spots and fungal blight, spray **Mancozeb 75% WP @ 2.5 g/liter** of water as a protective measure.\n"
            "• In case of high infestation, consider a systemic fungicide like **Azoxystrobin 23% SC @ 1 ml/liter**.\n"
            "• Use 5% Neem Seed Kernel Extract (NSKE) every 7-10 days for organic integrated pest management.\n"
            "⚠️ **Safety Note:** Always wear protective gear (mask and gloves) during application. Never spray against the wind."
        )
