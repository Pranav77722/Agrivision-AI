import uuid
import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_optional, get_current_user
from app.models.user import User
from app.repositories.conversation_repo import ConversationRepository
from app.schemas.conversation import (
    MessageCreate,
    ConversationResponse,
    ConversationSummaryResponse,
    VoiceChatRequest,
    VoiceChatResponse,
)
from app.services.assistant_service import AssistantService
from app.services.speech_service import BhashiniSpeechService
from app.services.storage_service import get_storage_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/assistant", tags=["AI Farming Assistant"])


@router.post(
    "/chat",
    response_model=ConversationResponse,
    summary="Chat with Agrivision AI+ Assistant",
    description="Send a message to Krishi Mitra and receive contextual agricultural guidance."
)
async def chat_message(
    msg_in: MessageCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> ConversationResponse:
    repo = ConversationRepository(db)
    user_id = current_user.id if current_user else None

    # Retrieve or create conversation
    conv = None
    if msg_in.conversation_id:
        conv = await repo.get_with_messages(msg_in.conversation_id)

    if not conv:
        conv = await repo.create(
            user_id=user_id,
            title=msg_in.content[:40] if len(msg_in.content) > 40 else msg_in.content,
            language=msg_in.language or "en"
        )
        conv = await repo.get_with_messages(conv.id)

    # Add user message
    await repo.add_message(
        conversation_id=conv.id,
        role="user",
        content=msg_in.content
    )

    # Prepare context
    farmer_ctx = None
    if current_user and current_user.profile:
        farmer_ctx = {
            "state": current_user.profile.state,
            "district": current_user.profile.district,
            "primary_crops": current_user.profile.primary_crops,
            "soil_type": current_user.profile.soil_type,
        }

    # Prepare chat history
    history = [{"role": m.role, "content": m.content} for m in conv.messages]

    # Generate response
    assistant_service = AssistantService()
    reply = await assistant_service.generate_response(
        user_message=msg_in.content,
        conversation_history=history,
        language=msg_in.language or "en",
        farmer_context=farmer_ctx
    )

    # Save assistant message
    await repo.add_message(
        conversation_id=conv.id,
        role="assistant",
        content=reply
    )

    # Reload conversation with all messages
    updated_conv = await repo.get_with_messages(conv.id)
    return ConversationResponse.model_validate(updated_conv)


@router.get(
    "/conversations",
    response_model=List[ConversationSummaryResponse],
    summary="List user conversations",
    description="Retrieve all previous advisory sessions initiated by the current farmer."
)
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[ConversationSummaryResponse]:
    repo = ConversationRepository(db)
    convs = await repo.list_for_user(user_id=current_user.id)
    results = []
    for c in convs:
        summary = ConversationSummaryResponse.model_validate(c)
        summary.message_count = len(c.messages)
        results.append(summary)
    return results


@router.get(
    "/conversations/{id}",
    response_model=ConversationResponse,
    summary="Get conversation thread",
    description="Retrieve complete message history of a specific conversation thread."
)
async def get_conversation(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> ConversationResponse:
    repo = ConversationRepository(db)
    conv = await repo.get_with_messages(id)
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )
    return ConversationResponse.model_validate(conv)


@router.post(
    "/voice",
    response_model=VoiceChatResponse,
    summary="Voice-based agricultural assistant",
    description="Process base64 voice audio from farmer, transcribe speech (STT), query Krishi Mitra, and synthesize spoken reply audio (TTS)."
)
async def voice_chat(
    req: VoiceChatRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> VoiceChatResponse:
    speech_service = BhashiniSpeechService()
    storage = get_storage_service()

    # 1. Transcribe voice input
    transcribed_text = await speech_service.speech_to_text(
        audio_content_base64=req.audio_base64,
        language=req.language
    )

    # 2. Process conversation
    repo = ConversationRepository(db)
    conv = None
    if req.conversation_id:
        conv = await repo.get_with_messages(req.conversation_id)

    if not conv:
        user_id = current_user.id if current_user else None
        conv = await repo.create(
            user_id=user_id,
            title=transcribed_text[:40],
            language=req.language
        )
        conv = await repo.get_with_messages(conv.id)

    # Add user message
    await repo.add_message(
        conversation_id=conv.id,
        role="user",
        content=transcribed_text
    )

    # 3. Query Assistant
    assistant_service = AssistantService()
    reply = await assistant_service.generate_response(
        user_message=transcribed_text,
        language=req.language
    )

    # 4. Generate audio reply (TTS)
    audio_bytes, mime = await speech_service.text_to_speech(reply, language=req.language)
    audio_url = await storage.upload_file(
        file_bytes=audio_bytes,
        filename=f"tts_{uuid.uuid4().hex}.wav",
        content_type=mime,
        folder="audio"
    )

    # Add assistant message
    await repo.add_message(
        conversation_id=conv.id,
        role="assistant",
        content=reply,
        audio_url=audio_url
    )

    return VoiceChatResponse(
        conversation_id=conv.id,
        transcribed_text=transcribed_text,
        assistant_reply=reply,
        audio_url=audio_url,
        language=req.language
    )
