from app.schemas import *


class RSSMessagePayload(RSSMessageBase):
    pass


class RSSMessageResponse(RSSMessageBase):
    id: int
    create_time: str


class SourcePayload(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: int
    create_time: str
