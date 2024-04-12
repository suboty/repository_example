from typing import List, Optional

from fastapi import Depends
from app.models.models import Sources

from app.repositories.sources import SourcesRepository
from app.schemas.schemas import SourcePayload


class SourcesService:
    sources_repository: SourcesRepository

    def __init__(
            self, sources_repository: SourcesRepository = Depends()
    ) -> None:
        self.sources_repository = sources_repository

    async def create(self, source_body: SourcePayload) -> Sources:
        return await self.sources_repository.create(
            Sources(
                source_name=source_body.source_name,
                source_description=source_body.source_description,
                site_url=source_body.site_url,
                rss_url=source_body.rss_url,
                source_hash=source_body.source_hash,
                source_time=source_body.source_time,
            )
        )

    async def delete(self, source_id: int) -> None:
        return await self.sources_repository.delete(
            Sources(id=source_id)
        )

    async def get(self, source_id: int) -> Sources:
        return await self.sources_repository.get(
            Sources(id=source_id)
        )

    async def list(
            self,
            page_size: Optional[int] = 100,
            start_index: Optional[int] = 0,
    ) -> List[Sources]:
        return await self.sources_repository.list(
            limit=page_size,
            start=start_index,
        )

    async def update(
            self, source_id: int, source_body: SourcePayload
    ) -> Sources:
        return await self.sources_repository.update(
            source_id, Sources(
                source_name=source_body.source_name,
                source_description=source_body.source_description,
                site_url=source_body.site_url,
                rss_url=source_body.rss_url,
                source_hash=source_body.source_hash,
                source_time=source_body.source_time,
            )
        )
