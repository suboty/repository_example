from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.logger import logger
from app.connect_to_db import get_db_connection
from app.models.models import Sources
from app.repositories import decorator_rollback_error


class SourcesRepository:
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
    ) -> List[Sources]:
        res = await self.db.execute(select(Sources).order_by(desc(Sources.create_time)).offset(start).limit(limit))
        logger.debug(f'Get Sources from <{start}> to <{limit}>')
        return [dict(x)['Sources'].normalize() for x in res.mappings().all()]

    @decorator_rollback_error
    async def get(self, source: Sources) -> Sources:
        res = await self.db.get(
            Sources,
            source.id,
        )
        logger.debug(f'Get Source with ID <{res.id}>')
        return res.normalize()

    @decorator_rollback_error
    async def create(self, source: Sources) -> Sources:
        source.source_time = datetime.strptime(source.source_time, "%Y-%m-%d %H:%M:%S")
        self.db.add(source)
        await self.db.commit()
        await self.db.refresh(source)
        logger.debug(f'Create Source with name <{source.source_name}>')
        return source.normalize()

    @decorator_rollback_error
    async def update(self, _id: int, source: Sources) -> Sources:
        source.source_time = datetime.strptime(source.source_time, "%Y-%m-%d %H:%M:%S")
        source.id = _id
        await self.db.merge(source)
        await self.db.commit()
        logger.debug(f'Update Source with ID <{_id}>')
        return source.normalize()

    @decorator_rollback_error
    async def delete(self, source: Sources) -> None:
        row = await self.db.execute(select(Sources).where(Sources.id == source.id))
        await self.db.delete(row.scalar_one())
        await self.db.commit()
        await self.db.flush()
        logger.debug(f'Delete Source with ID <{source.id}>')
