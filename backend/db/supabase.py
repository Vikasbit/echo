"""
Echo — Supabase Client
Initializes and manages the Supabase connection.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from supabase import create_client
from supabase.client import Client

from backend.core.config import get_settings
from backend.core.logging import get_logger

logger = get_logger(__name__)

_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """Get or create the Supabase client singleton."""
    global _client

    if _client is not None:
        return _client

    settings = get_settings()

    if not settings.supabase_url or not settings.supabase_key:
        logger.warning(
            "supabase_not_configured",
            message="Supabase credentials not set. Running in demo mode.",
        )
        raise RuntimeError("Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY.")

    _client = create_client(settings.supabase_url, settings.supabase_key)
    logger.info("supabase_connected", url=settings.supabase_url)
    return _client


def get_supabase_admin() -> Client:
    """Get Supabase client with service role key for admin operations."""
    settings = get_settings()

    if not settings.supabase_url or not settings.supabase_service_key:
        raise RuntimeError("Supabase service key not configured.")

    return create_client(settings.supabase_url, settings.supabase_service_key)


class SupabaseRepository:
    """Base repository providing Supabase table access."""

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name
        self._client: Optional[Client] = None

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = get_supabase_client()
        return self._client

    @property
    def table(self):
        return self.client.table(self.table_name)

    @property
    def storage(self):
        return self.client.storage
