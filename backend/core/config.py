"""
INDUS AI — Application Configuration
Pydantic Settings with environment variable loading.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(Path(__file__).resolve().parent.parent, ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ───────────────────────────────────────────────────────
    app_name: str = "INDUS AI"
    app_env: str = "development"
    app_debug: bool = True
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # ── Supabase ──────────────────────────────────────────────────
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""

    # ── OpenAI ────────────────────────────────────────────────────
    openai_api_key: str = ""

    # ── JWT ───────────────────────────────────────────────────────
    jwt_secret_key: str = "indus-ai-dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440  # 24 hours

    # ── CORS ──────────────────────────────────────────────────────
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # ── Upload ────────────────────────────────────────────────────
    upload_max_size_mb: int = 50
    upload_bucket: str = "documents"

    # ── AI ────────────────────────────────────────────────────────
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    chat_model: str = "gpt-4o"
    chat_max_tokens: int = 4096
    chunk_size: int = 512
    chunk_overlap: int = 64
    similarity_top_k: int = 8

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def upload_max_bytes(self) -> int:
        return self.upload_max_size_mb * 1024 * 1024


@lru_cache()
def get_settings() -> Settings:
    return Settings()
