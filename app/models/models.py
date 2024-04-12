from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, ARRAY
from sqlalchemy.sql import func

from app.models import EntityMeta


class RSSMessages(EntityMeta):
    __tablename__ = 'rss_messages'

    id = Column(BigInteger, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tags_array = Column(ARRAY(String), nullable=True)
    categories_array = Column(ARRAY(String), nullable=True)
    enclosures_tuples = Column(ARRAY(String), nullable=True)
    author = Column(String, nullable=True)
    guid = Column(String, nullable=False)
    public_time = Column(TIMESTAMP, nullable=False)
    source_time = Column(TIMESTAMP, nullable=False)
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), index=True)
    source_hash = Column(String, nullable=False, server_default='')

    def normalize(self):
        return {
            "id": self.id,
            "link": self.link.__str__(),
            "title": self.title.__str__(),
            "description": self.description.__str__(),
            "tags_array": self.tags_array,
            "categories_array": self.categories_array,
            "enclosures_tuples": self.enclosures_tuples,
            "author": self.author.__str__(),
            "guid": self.guid.__str__(),
            "public_time": self.public_time.__str__(),
            "source_time": self.source_time.__str__(),
            "create_time": self.create_time.__str__(),
            "source_hash": self.source_hash.__str__(),
        }


class Sources(EntityMeta):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    source_name = Column(String, nullable=False)
    source_description = Column(String, nullable=False)
    site_url = Column(String, nullable=False)
    rss_url = Column(String, nullable=True)
    source_time = Column(TIMESTAMP, nullable=False)
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), index=True)
    source_hash = Column(String, nullable=False, server_default='')

    def normalize(self):
        return {
            "id": self.id,
            "source_name": self.source_name.__str__(),
            "source_description": self.source_description.__str__(),
            "site_url": self.site_url.__str__(),
            "rss_url": self.rss_url.__str__(),
            "source_time": self.source_time.__str__(),
            "create_time": self.create_time.__str__(),
            "source_hash": self.source_hash.__str__(),
        }


