"""
Echo — Search API
Endpoints for the unified command palette search.
"""

import time
from fastapi import APIRouter, Depends
from backend.schemas.search import SearchRequest, SearchResponse
from backend.schemas.base import ApiResponse
from backend.db.supabase import get_supabase_client
from backend.core.dependencies import get_current_user_id

router = APIRouter()


@router.post("", response_model=ApiResponse[SearchResponse])
async def search_all(
    request: SearchRequest,
    user_id: str = Depends(get_current_user_id)
):
    start_time = time.perf_counter()
    client = get_supabase_client()
    
    result = client.rpc(
        "unified_search",
        {
            "search_query": request.query,
            "filter_user_id": user_id,
            "result_limit": request.limit
        }
    ).execute()
    
    query_time_ms = (time.perf_counter() - start_time) * 1000
    
    # Map raw RPC results to the Pydantic schema
    results = []
    if result.data:
        for r in result.data:
            # Generate URL based on type
            url = ""
            if r["result_type"] == "document":
                url = f"/documents/{r['result_id']}"
            elif r["result_type"] == "equipment":
                url = f"/equipment/{r['result_id']}"
            elif r["result_type"] == "conversation":
                url = f"/chat/{r['result_id']}"
                
            results.append({
                "id": r["result_id"],
                "type": r["result_type"],
                "title": r["title"],
                "excerpt": r.get("excerpt", ""),
                "relevance": r.get("relevance", 0.0),
                "url": url
            })
            
    response_data = {
        "results": results,
        "query_time_ms": query_time_ms
    }
    
    return ApiResponse(data=response_data)
