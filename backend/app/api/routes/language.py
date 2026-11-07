import uuid
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services.translation_service import TranslationService
from app.services.speech_service import BhashiniSpeechService
from app.services.storage_service import get_storage_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/language", tags=["Multilingual & Speech Services"])


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1)
    target_lang: str = Field(..., pattern="^(en|mr|hi)$")
    source_lang: Optional[str] = Field(None, pattern="^(en|mr|hi)$")


class TranslateResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1)
    language: str = Field(default="mr", pattern="^(en|mr|hi)$")


class TTSResponse(BaseModel):
    audio_url: str
    language: str


class STTRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64-encoded audio (WAV/MP3)")
    language: str = Field(default="mr", pattern="^(en|mr|hi)$")


class STTResponse(BaseModel):
    transcribed_text: str
    language: str


@router.post(
    "/translate",
    response_model=TranslateResponse,
    summary="Translate agricultural text",
    description="Translate farming advisories and descriptions between English, Marathi, and Hindi using Bhashini and IndicTrans2."
)
async def translate_text(req: TranslateRequest) -> TranslateResponse:
    service = TranslationService()
    detected_source = req.source_lang or service.detect_language(req.text)
    translated = await service.translate_text(
        text=req.text,
        target_lang=req.target_lang,
        source_lang=detected_source
    )
    return TranslateResponse(
        translated_text=translated,
        source_lang=detected_source,
        target_lang=req.target_lang
    )


@router.post(
    "/tts",
    response_model=TTSResponse,
    summary="Text to speech",
    description="Synthesize spoken audio from agricultural text in Marathi, Hindi, or English."
)
async def text_to_speech(req: TTSRequest) -> TTSResponse:
    speech_service = BhashiniSpeechService()
    storage = get_storage_service()

    audio_bytes, mime = await speech_service.text_to_speech(req.text, language=req.language)
    audio_url = await storage.upload_file(
        file_bytes=audio_bytes,
        filename=f"tts_{uuid.uuid4().hex}.wav",
        content_type=mime,
        folder="audio"
    )

    return TTSResponse(audio_url=audio_url, language=req.language)


@router.post(
    "/stt",
    response_model=STTResponse,
    summary="Speech to text",
    description="Convert recorded voice speech into Marathi, Hindi, or English text."
)
async def speech_to_text(req: STTRequest) -> STTResponse:
    speech_service = BhashiniSpeechService()
    text = await speech_service.speech_to_text(req.audio_base64, language=req.language)
    return STTResponse(transcribed_text=text, language=req.language)
