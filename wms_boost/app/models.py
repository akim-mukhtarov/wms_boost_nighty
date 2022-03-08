from app.db import Base
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Enum as DbEnum
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Unicode,
    DateTime
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


class LastRefundsDump(Base):
    __tablename__ = "refunds_dumps"

    id = Column(Integer, primary_key=True, index=True)
    workplace_id = Column(Integer, ForeignKey("workplaces.wms_key"))

    report_url = Column(String(256))
    included = Column(Integer, default=0)
    processed = Column(Integer, default=0)

    date = Column(DateTime, nullable=True)
    status_choices = Enum('status_choices', 'default enqueued completed')
    status = Column(
        DbEnum(status_choices),
        nullable=False,
        default=status_choices.default
    )


class StorageStepsProgress(Base):
    __tablename__ = "storage_steps"

    id = Column(Integer, primary_key=True, index=True)
    workplace_id = Column(Integer, ForeignKey("workplaces.wms_key"))

    report_url = Column(String(256))
    included = Column(Integer, default=0)
    processed = Column(Integer, default=0)

    last_run = Column(DateTime, nullable=True)
    last_completion = Column(DateTime, nullable=True)

    status_choices = Enum('status_choices', [
        'default',
        'enqueued',
        'accepted',
        'completed'
    ])
    status = Column(
        DbEnum(status_choices),
        nullable=False,
        default=status_choices.default
    )


class Workplace(Base):
    __tablename__ = "workplaces"

    wms_key = Column(Integer, primary_key=True, index=True)
    short_name = Column(Unicode(8))
    timezone = Column(String(32))

    last_refunds_dump = relationship(
        "LastRefundsDump",
        backref="workplace",
        uselist=False)

    storage_steps_progress = relationship(
        "StorageStepsProgress",
        backref="workplace",
        uselist=False)
