"""
Echo — Chat API
Endpoints for RAG chat and streaming.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from backend.schemas.chat import CreateConversationRequest, SendMessageRequest, ConversationResponse
from backend.schemas.base import ApiResponse
from backend.services.chat_service import ChatService
from backend.db.repositories.conversation_repo import ConversationRepository
from backend.core.dependencies import get_current_user_id

router = APIRouter()
conv_repo = ConversationRepository()


@router.post("/conversations", response_model=ApiResponse[ConversationResponse])
async def create_conversation(
    request: CreateConversationRequest,
    user_id: str = Depends(get_current_user_id)
):
    conv = await conv_repo.create({
        "user_id": user_id,
        "title": request.title
    })
    return ApiResponse(data=conv)


@router.get("/conversations", response_model=ApiResponse[list])
async def list_conversations(user_id: str = Depends(get_current_user_id)):
    convs = await conv_repo.list_by_user(user_id)
    return ApiResponse(data=convs)


@router.post("/conversations/{conversation_id}/messages")
async def send_message(
    conversation_id: str,
    request: SendMessageRequest,
    req: Request,
    user_id: str = Depends(get_current_user_id)
):
    service = ChatService()
    
    # Stream the SSE response
    return StreamingResponse(
        service.chat_stream(conversation_id, request.content, user_id),
        media_type="text/event-stream"
    )
