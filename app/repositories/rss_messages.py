from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.logger import logger
from app.connect_to_db import get_db_connection
from app.models.models import RSSMessages
from app.repositories import decorator_rollback_error


class RSSMessagesRepository:
    db: AsyncSession

    def __init__(
            self, db: AsyncSession = Depends(get_db_connection)
    ) -> None:
        self.db = db

    @decorator_rollback_error
    async def list(
            self,
            limit: Optional[int],
            start: Optional[int],
    ) -> List[RSSMessages]:
        res = await self.db.execute(select(
            RSSMessages).order_by(desc(RSSMessages.create_time)).offset(start).limit(limit))
        logger.debug(f'Get RSS messages from <{start}> to <{limit}>')
        return [dict(x)['RSSMessages'].normalize() for x in res.mappings().all()]

    @decorator_rollback_error
    async def get(self, message: RSSMessages) -> RSSMessages:
        res = await self.db.get(
            RSSMessages,
            message.id,
        )
        logger.debug(f'Get Message with ID <{res.id}>')
        return res.normalize()

    @decorator_rollback_error
    async def create(self, message: RSSMessages) -> RSSMessages:
        message.source_time = datetime.strptime(message.source_time, "%Y-%m-%d %H:%M:%S")
        message.public_time = datetime.strptime(message.public_time, "%Y-%m-%d %H:%M:%S")
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        logger.debug(f'Create Message with title <{message.title}>')
        return message.normalize()

    @decorator_rollback_error
    async def update(self, _id: int, message: RSSMessages) -> RSSMessages:
        message.source_time = datetime.strptime(message.source_time, "%Y-%m-%d %H:%M:%S")
        message.public_time = datetime.strptime(message.public_time, "%Y-%m-%d %H:%M:%S")
        message.id = _id
        await self.db.merge(message)
        await self.db.commit()
        logger.debug(f'Update Message with ID <{_id}>')
        return message.normalize()

    @decorator_rollback_error
    async def delete(self, message: RSSMessages) -> None:
        row = await self.db.execute(select(RSSMessages).where(RSSMessages.id == message.id))
        await self.db.delete(row.scalar_one())
        await self.db.commit()
        await self.db.flush()
        logger.debug(f'Delete Message with ID <{message.id}>')
