"""
Echo — Chat Schemas
Request and response models for chat/conversation endpoints.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ConversationResponse(BaseModel):
    id: str
    title: str
    last_message: Optional[str] = None
    message_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class CreateConversationRequest(BaseModel):
    title: str = Field(default="New Conversation", min_length=1, max_length=200)


class SourceCitation(BaseModel):
    document_id: str
    document_title: str
    page_number: Optional[int] = None
    excerpt: str
    relevance_score: float = 0.0


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    sources: List[SourceCitation] = Field(default_factory=list)
    created_at: Optional[str] = None


class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    """Response from the AI chat endpoint."""

    message: MessageResponse
    sources: List[SourceCitation] = Field(default_factory=list)
