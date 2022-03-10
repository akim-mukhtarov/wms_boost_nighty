from app.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Unicode
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(Unicode(32))
    last_name = Column(Unicode(32))

    wms_access_token = Column(String(128))
    wms_refresh_token = Column(String(128))

    def update_tokens(self, access_token: str, refresh_token: str):
        self.wms_access_token = access_token
        self.wms_refresh_token = refresh_token


class RefundsDumpSettings(Base):
    __tablename__ = "refunds_dumps_settings"

    id = Column(Integer, primary_key=True, index=True)
    workplace_id = Column(Integer, ForeignKey("workplaces.wms_key"))
    report_url = Column(String(256))
    redis_key = Column(String(32))

    @classmethod
    def generate_redis_key(cls, workplace_id: int) -> str:
        return f'{workplace_id}_{cls.__tablename__}'


class StorageStepsSettings(Base):
    __tablename__ = "storage_steps_settings"

    id = Column(Integer, primary_key=True, index=True)
    workplace_id = Column(Integer, ForeignKey("workplaces.wms_key"))
    report_url = Column(String(256))
    redis_key = Column(String(32))

    @classmethod
    def generate_redis_key(cls, workplace_id: int) -> str:
        return f'{workplace_id}_{cls.__tablename__}'


class Workplace(Base):
    __tablename__ = "workplaces"

    wms_key = Column(Integer, primary_key=True, index=True)
    short_name = Column(Unicode(8))
    timezone = Column(String(32))

    refunds_dump_settings = relationship(
        "RefundsDumpSettings",
        backref="workplace",
        uselist=False)

    storage_steps_settings = relationship(
        "StorageStepsSettings",
        backref="workplace",
        uselist=False)
