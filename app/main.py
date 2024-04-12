import asyncio
from pathlib import Path

from fastapi import FastAPI

from app.logger import logger
from app.models import init
from app.connect_to_db import get_engine_and_session, get_environment_db_variables
from app.routers.sources import SourcesRouter
from app.routers.rss_messages import RSSMessagesRouter

app = FastAPI(
    title='Repository Pattern Example',
    version='0.1.0',
    openapi_tags=[
        {
            "name": "rss_messages",
            "description": "Contains CRUD methods for RSS Messages entity",
        },
        {
            "name": "sources",
            "description": "Contains CRUD methods for Sources entity",
        },
    ],
)

app.include_router(SourcesRouter)
app.include_router(RSSMessagesRouter)


async def init_app():

    env = get_environment_db_variables(Path('app', '.env'))

    connect_tasks = [
        asyncio.wait_for(asyncio.create_task(get_engine_and_session(env=env)), timeout=20),
    ]

    try:
        await asyncio.gather(*connect_tasks)
    except asyncio.TimeoutError:
        logger.critical("Timeout for databases connection, aborting")
        exit(0)

    init_tasks = [
        asyncio.wait_for(asyncio.create_task(init()), timeout=20),
    ]

    try:
        await asyncio.gather(*init_tasks)
    except asyncio.TimeoutError:
        logger.critical("Timeout for databases initialization, aborting")
        exit(0)


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.get_event_loop()

loop.create_task(init_app())
