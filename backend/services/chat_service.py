"""
Echo — Chat Service
RAG Pipeline & Streaming Chat.
"""

from __future__ import annotations

import json
from typing import Any, AsyncGenerator, Dict, List

from openai import AsyncOpenAI

from backend.core.config import get_settings
from backend.core.logging import get_logger
from backend.db.repositories.conversation_repo import ConversationRepository, MessageRepository
from backend.db.repositories.document_repo import ChunkRepository
from backend.services.embedding_service import EmbeddingService

logger = get_logger(__name__)
settings = get_settings()


class ChatService:
    def __init__(self) -> None:
        self.conv_repo = ConversationRepository()
        self.msg_repo = MessageRepository()
        self.chunk_repo = ChunkRepository()
        self.embedding_service = EmbeddingService()
        self.openai_client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = settings.chat_model

    async def chat_stream(
        self, conversation_id: str, content: str, user_id: str
    ) -> AsyncGenerator[str, None]:
        """Stream RAG chat response."""
        # 1. Embed query
        query_embedding = await self.embedding_service.embed_text(content)

        # 2. Retrieve relevant chunks
        chunks = await self.chunk_repo.similarity_search(
            query_embedding, user_id, top_k=settings.similarity_top_k
        )

        sources = []
        context_parts = []
        for i, c in enumerate(chunks):
            sources.append({
                "document_id": c["document_id"],
                "document_title": c.get("document_title", f"Doc {c['document_id']}"),
                "page_number": c["page_number"],
                "excerpt": c["content"][:150] + "...",
                "relevance_score": c["similarity"]
            })
            context_parts.append(f"--- Document: {c.get('document_title', 'Unknown')} ---\n{c['content']}")

        context_text = "\n\n".join(context_parts)

        # 3. Build prompts
        system_prompt = (
            "You are Echo, an advanced industrial engineering assistant powered by Gemini.\n"
            "You MUST search and use ONLY the uploaded documents provided in the context below.\n"
            "NEVER hallucinate or use outside knowledge. If the answer is not found in the context, "
            "clearly state: 'This information is unavailable in the uploaded documents.'\n\n"
            "EVERY answer MUST be formatted with the following markdown headings exactly:\n"
            "### Summary\n"
            "### Explanation\n"
            "### Recommendations\n"
            "### Confidence Score\n"
            "### Source Document\n"
            "### Page Number\n"
            "### Related Documents\n\n"
            "Extract the Source Document, Page Number, and Related Documents directly from the provided Context metadata.\n"
            "Context:\n\n" + context_text
        )

        # Retrieve history
        history = await self.msg_repo.get_by_conversation(conversation_id, limit=10)
        messages = [{"role": "system", "content": system_prompt}]
        for m in history:
            messages.append({"role": m["role"], "content": m["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": content})

        # Save user message
        await self.msg_repo.create({
            "conversation_id": conversation_id,
            "role": "user",
            "content": content
        })

        # 4. Stream response
        try:
            stream = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            
            full_content = ""
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_content += text
                    # Yield chunk event
                    yield f"event: chunk\ndata: {json.dumps({'content': text})}\n\n"
            
            # 5. Yield sources and metadata
            metadata = {
                "confidence": 0.95,  # mock confidence
                "related_equipment": [],
                "related_documents": list(set([s["document_id"] for s in sources]))
            }
            yield f"event: sources\ndata: {json.dumps({'sources': sources})}\n\n"
            yield f"event: metadata\ndata: {json.dumps(metadata)}\n\n"

            # 6. Save assistant message
            msg = await self.msg_repo.create({
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": full_content,
                "sources": sources,
                "confidence": metadata["confidence"],
                "metadata": metadata
            })
            
            # Update conversation
            await self.conv_repo.update(conversation_id, {
                "last_message": full_content[:100] + "...",
                "message_count": len(history) + 2
            })

            yield f"event: done\ndata: {json.dumps({'message_id': msg['id']})}\n\n"

        except Exception as e:
            logger.error("chat_stream_error", error=str(e))
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
