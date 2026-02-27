from __future__ import annotations

from datetime import timedelta
from typing import Any

try:
    import redis.asyncio as redis
except Exception:
    redis = None

from app.models import NarrativeGraph


class NarrativeCache:
    def __init__(self, redis_url: str = "redis://localhost:6379") -> None:
        self.redis_url = redis_url
        self.redis = None
        self.default_ttl = timedelta(days=30)

    async def initialize(self) -> None:
        if redis is None:
            self.redis = None
            return
        self.redis = redis.from_url(self.redis_url, decode_responses=True)

    async def get_graph(self, reference: str, resource_id: str) -> NarrativeGraph | None:
        if self.redis is None:
            return None
        key = f"graph:{resource_id}:{reference}"
        value = await self.redis.get(key)
        if not value:
            return None
        return NarrativeGraph.model_validate_json(value)

    async def set_graph(self, reference: str, resource_id: str, graph: NarrativeGraph) -> None:
        if self.redis is None:
            return
        key = f"graph:{resource_id}:{reference}"
        await self.redis.set(key, graph.model_dump_json(), ex=int(self.default_ttl.total_seconds()))

    async def get_stats(self) -> dict[str, Any]:
        if self.redis is None:
            return {"connected": False}
        info = await self.redis.info()
        return {
            "connected": True,
            "used_memory": info.get("used_memory_human", "unknown"),
            "total_keys": await self.redis.dbsize(),
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
        }

    async def close(self) -> None:
        if self.redis is not None:
            await self.redis.aclose()
