from typing import List, Optional

from fastapi import Depends
from app.models.models import RSSMessages

from app.repositories.rss_messages import RSSMessagesRepository
from app.schemas.schemas import RSSMessagePayload


class RSSMessagesService:
    rss_messages_repository: RSSMessagesRepository

    def __init__(
            self, rss_messages_repository: RSSMessagesRepository = Depends()
    ) -> None:
        self.rss_messages_repository = rss_messages_repository

    async def create(self, message_body: RSSMessagePayload) -> RSSMessages:
        return await self.rss_messages_repository.create(
            RSSMessages(
                link=message_body.link,
                title=message_body.title,
                description=message_body.description,
                tags_array=message_body.tags_array,
                categories_array=message_body.categories_array,
                enclosures_tuples=message_body.enclosures_tuples,
                author=message_body.author,
                guid=message_body.guid,
                source_hash=message_body.source_hash,
                source_time=message_body.source_time,
                public_time=message_body.public_time,
            )
        )

    async def delete(self, message_id: int) -> None:
        return await self.rss_messages_repository.delete(
            RSSMessages(id=message_id)
        )

    async def get(self, message_id: int) -> RSSMessages:
        return await self.rss_messages_repository.get(
            RSSMessages(id=message_id)
        )

    async def list(
            self,
            page_size: Optional[int] = 100,
            start_index: Optional[int] = 0,
    ) -> List[RSSMessages]:
        return await self.rss_messages_repository.list(
            limit=page_size,
            start=start_index,
        )

    async def update(
            self, message_id: int, message_body: RSSMessagePayload
    ) -> RSSMessages:
        return await self.rss_messages_repository.update(
            message_id, RSSMessages(
                link=message_body.link,
                title=message_body.title,
                description=message_body.description,
                tags_array=message_body.tags_array,
                categories_array=message_body.categories_array,
                enclosures_tuples=message_body.enclosures_tuples,
                author=message_body.author,
                guid=message_body.guid,
                source_hash=message_body.source_hash,
                source_time=message_body.source_time,
                public_time=message_body.public_time,
            )
        )
