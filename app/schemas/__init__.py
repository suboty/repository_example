from typing import Optional, List
from pydantic import BaseModel


class RSSMessageBase(BaseModel):
    link: str
    title: str
    description: str
    tags_array: Optional[List[str]]
    categories_array: Optional[List[str]]
    enclosures_tuples: Optional[List[str]]
    author: Optional[str]
    guid: str
    source_hash: str
    public_time: str
    source_time: str

    class Config:
        orm_mode = True


class SourceBase(BaseModel):
    source_name: str
    source_description: str
    site_url: str
    rss_url: Optional[str]
    source_hash: str
    source_time: str

    class Config:
        orm_mode = True

