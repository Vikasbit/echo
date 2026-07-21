"""
Echo — Embedding Service
Generates vector embeddings using Gemini text-embedding-004.
"""

from __future__ import annotations

from typing import List

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.core.config import get_settings
from backend.core.exceptions import ExternalServiceError
from backend.core.logging import get_logger

logger = get_logger(__name__)

settings = get_settings()


class EmbeddingService:
    """Generates embeddings via OpenAI API."""

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = settings.embedding_model
        self.dimensions = settings.embedding_dimensions

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def embed_text(self, text: str) -> List[float]:
        """Generate an embedding vector for a single text string."""
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self.model,
                dimensions=self.dimensions,
            )
            embedding = response.data[0].embedding
            logger.debug("embedding_generated", model=self.model, dimensions=len(embedding))
            return embedding
        except Exception as e:
            logger.error("embedding_failed", error=str(e))
            raise ExternalServiceError("OpenAI Embeddings", str(e))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for a batch of texts.

        Gemini supports batching through the OpenAI compatible endpoint. We chunk into batches
        of `batch_size` to stay within API limits.
        """
        all_embeddings: List[List[float]] = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            try:
                response = await self.client.embeddings.create(
                    input=batch,
                    model=self.model,
                    dimensions=self.dimensions,
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
                logger.info(
                    "batch_embeddings_generated",
                    batch_index=i // batch_size,
                    count=len(batch_embeddings),
                )
            except Exception as e:
                logger.error("batch_embedding_failed", batch_index=i // batch_size, error=str(e))
                raise ExternalServiceError("OpenAI Embeddings", str(e))

        return all_embeddings
