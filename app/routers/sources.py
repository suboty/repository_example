from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.schemas import *
from app.services.sources import SourcesService


SourcesRouter = APIRouter(
    prefix="/v0/sources", tags=["sources"]
)


@SourcesRouter.get("/", response_model=List[SourceResponse])
async def index(
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    sources_service: SourcesService = Depends(),
):
    return [
        source
        for source in await sources_service.list(
            page_size=page_size,
            start_index=start_index,
        )
    ]


@SourcesRouter.get("/{source_id}", response_model=SourceResponse)
async def get(source_id: int, sources_service: SourcesService = Depends()):
    try:
        return await sources_service.get(source_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Source with ID {source_id} is not found")


@SourcesRouter.post(
    "/",
    response_model=SourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    source: SourcePayload,
    sources_service: SourcesService = Depends(),
):
    return await sources_service.create(source)


@SourcesRouter.patch("/{source_id}", response_model=SourceResponse)
async def update(
    source_id: int,
    source: SourcePayload,
    sources_service: SourcesService = Depends(),
):
    return await sources_service.update(source_id, source)


@SourcesRouter.delete(
    "/{source_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    source_id: int, sources_service: SourcesService = Depends()
):
    return await sources_service.delete(source_id)
