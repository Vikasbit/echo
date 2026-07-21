"""
Echo — Chat Routes
Conversation and message endpoints with RAG-powered AI responses.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.core.dependencies import CurrentUser
from backend.core.logging import get_logger
from backend.schemas.base import ApiResponse
from backend.schemas.chat import (
    ChatResponse,
    ConversationResponse,
    CreateConversationRequest,
    MessageResponse,
    SendMessageRequest,
    SourceCitation,
)
from backend.services.chat_service import ChatService

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat"])

chat_service = ChatService()


@router.get("/conversations", response_model=ApiResponse[list[ConversationResponse]])
async def list_conversations(user_id: CurrentUser):
    """List all conversations for the current user."""
    conversations = await chat_service.get_conversations(user_id)

    return ApiResponse(
        data=[
            ConversationResponse(
                id=c["id"],
                title=c.get("title", "New Conversation"),
                last_message=c.get("last_message"),
                message_count=c.get("message_count", 0),
                created_at=c.get("created_at"),
                updated_at=c.get("updated_at"),
            )
            for c in conversations
        ]
    )


@router.post("/conversations", response_model=ApiResponse[ConversationResponse])
async def create_conversation(request: CreateConversationRequest, user_id: CurrentUser):
    """Create a new conversation."""
    conversation = await chat_service.create_conversation(user_id, request.title)

    return ApiResponse(
        data=ConversationResponse(
            id=conversation["id"],
            title=conversation["title"],
            message_count=0,
            created_at=conversation.get("created_at"),
            updated_at=conversation.get("updated_at"),
        ),
        message="Conversation created",
    )


@router.get("/conversations/{conversation_id}", response_model=ApiResponse[list[MessageResponse]])
async def get_conversation_messages(conversation_id: str, user_id: CurrentUser):
    """Get all messages in a conversation."""
    messages = await chat_service.get_messages(conversation_id)

    return ApiResponse(
        data=[
            MessageResponse(
                id=m["id"],
                conversation_id=m["conversation_id"],
                role=m["role"],
                content=m["content"],
                sources=[SourceCitation(**s) for s in (m.get("sources") or [])],
                created_at=m.get("created_at"),
            )
            for m in messages
        ]
    )


@router.post("/conversations/{conversation_id}/messages", response_model=ApiResponse[ChatResponse])
async def send_message(
    conversation_id: str,
    request: SendMessageRequest,
    user_id: CurrentUser,
):
    """Send a message and receive an AI response with source citations.

    This endpoint:
    1. Saves the user message
    2. Performs semantic search across indexed documents
    3. Sends context + query to GPT
    4. Returns AI response with document citations
    """
    result = await chat_service.send_message(
        conversation_id=conversation_id,
        user_id=user_id,
        content=request.content,
    )

    ai_msg = result["message"]
    sources = result["sources"]

    return ApiResponse(
        data=ChatResponse(
            message=MessageResponse(
                id=ai_msg["id"],
                conversation_id=ai_msg["conversation_id"],
                role=ai_msg["role"],
                content=ai_msg["content"],
                sources=[SourceCitation(**s) for s in sources],
                created_at=ai_msg.get("created_at"),
            ),
            sources=[SourceCitation(**s) for s in sources],
        )
    )


@router.delete("/conversations/{conversation_id}", response_model=ApiResponse)
async def delete_conversation(conversation_id: str, user_id: CurrentUser):
    """Delete a conversation and all its messages."""
    await chat_service.delete_conversation(conversation_id)
    return ApiResponse(message="Conversation deleted")
