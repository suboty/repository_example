from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.schemas import *
from app.services.rss_messages import RSSMessagesService


RSSMessagesRouter = APIRouter(
    prefix="/v0/rss_messages", tags=["rss_messages"]
)


@RSSMessagesRouter.get("/", response_model=List[RSSMessageResponse])
async def index(
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    rss_messages_service: RSSMessagesService = Depends(),
):
    return [
        message
        for message in await rss_messages_service.list(
            page_size=page_size,
            start_index=start_index,
        )
    ]


@RSSMessagesRouter.get("/{message_id}", response_model=RSSMessageResponse)
async def get(message_id: int, rss_messages_service: RSSMessagesService = Depends()):
    try:
        return await rss_messages_service.get(message_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Message with ID {message_id} is not found")


@RSSMessagesRouter.post(
    "/",
    response_model=RSSMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    message: RSSMessagePayload,
    rss_messages_service: RSSMessagesService = Depends(),
):
    return await rss_messages_service.create(message)


@RSSMessagesRouter.patch("/{message_id}", response_model=RSSMessageResponse)
async def update(
    message_id: int,
    message: RSSMessagePayload,
    rss_messages_service: RSSMessagesService = Depends(),
):
    return await rss_messages_service.update(message_id, message)


@RSSMessagesRouter.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    message_id: int, rss_messages_service: RSSMessagesService = Depends()
):
    return await rss_messages_service.delete(message_id)
