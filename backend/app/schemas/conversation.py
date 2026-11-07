import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    conversation_id: Optional[uuid.UUID] = None
    content: str = Field(..., min_length=1)
    language: Optional[str] = Field(default="en", pattern="^(en|mr|hi)$")


class MessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    audio_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationCreate(BaseModel):
    title: Optional[str] = "Crop Advisory Conversation"
    language: Optional[str] = Field(default="en", pattern="^(en|mr|hi)$")


class ConversationSummaryResponse(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    title: str
    language: str
    created_at: datetime
    message_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class ConversationResponse(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    title: str
    language: str
    created_at: datetime
    messages: List[MessageResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class VoiceChatRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64-encoded audio data")
    conversation_id: Optional[uuid.UUID] = None
    language: str = Field(default="mr", pattern="^(en|mr|hi)$")


class VoiceChatResponse(BaseModel):
    conversation_id: uuid.UUID
    transcribed_text: str
    assistant_reply: str
    audio_url: Optional[str] = None
    language: str
