'''
from __future__ import annotations
from typing import TypeVar, Optional, Callable, Dict, Awaitable
from datetime import datetime
from fastapi import WebSocket

from app.db import get_db
from app.models import (
    Workplace,
    LastRefundsDump,
    StorageStepsProgress
)

import asyncio
import pydantic
'''
'''
class WorkplaceResources(pydantic.BaseModel):
    """ Represents fields of workplace
        and its related resources to observe """
    short_name: str
    timezone: str

    class RefundsDump(pydantic.BaseModel):
        report_url: str
        included: int
        processed: int

        date: Optional[datetime]
        status: LastRefundsDump.status_choices

        class Config:
            orm_mode=True
            use_enum_values=True

    class StorageSteps(pydantic.BaseModel):
        report_url: str
        included: int
        processed: int

        last_run: Optional[datetime]
        last_completion: Optional[datetime]
        status: StorageStepsProgress.status_choices

        class Config:
            orm_mode=True
            use_enum_values=True

    last_refunds_dump: WorkplaceResources.RefundsDump
    storage_steps_progress: WorkplaceResources.StorageSteps

    class Config:
        orm_mode=True


AsyncCallback = TypeVar('AsyncCallback', bound=Callable[[Dict], Awaitable[None]])
OptionalCallback = TypeVar('OptionalCallback', bound=Optional[Callable])

# helper
def _lists_content_equals(fst, snd) -> bool:
    equals = map(
        lambda values: values[0] == values[1],
        zip(fst, snd)
    )
    return all(equals)


class WorkplaceObserver:
    """ Will periodically check `Workplace` in database
        and call back on changes """
    def __init__(self, workplace_id: int):
        self._workplace_id = workplace_id
        self._last_state = {}
        self._callback = None
        self._is_alive = None

    def on_update(self, callback: AsyncCallback) -> WorkplaceObserver:
        self._callback = callback
        return self

    def check_alive(self, alive: OptionalCallback) -> WorkplaceObserver:
        self._is_alive = alive
        return self

    def _get_workplace(self):
        db = next(iter(get_db()))
        workplace = db.query(Workplace).get(self._workplace_id)
        return workplace

    @staticmethod
    def _differs(fst, snd) -> bool:
        """ Check if values of two fields are not equal
            assume:
                - no nested dicts
                - type(fst) == type(snd) """
        assert (
            type(fst) is type(snd)
        ), "Fields to compare must be of the same type"

        if isinstance(fst, dict):
            # as of the python >= 3.7, values are ordered
            # so we can compare lists of values
            return not _lists_content_equals(
                fst.values(), snd.values())
        else:
            # assume some 'primitive' type
            return fst != snd

    def _check_updates(self):
        workplace = self._get_workplace()
        state_dict = WorkplaceResources.from_orm(workplace).dict()
        # just a dict of changes
        diff = {
            k : v
                for k, v in (
                    (k, state_dict[k])
                        for k in self._last_state
                            if self._differs(
                                state_dict[k], self._last_state[k])
                )
        }
        if len(diff):
            self._last_state = state_dict
        return diff

    async def poll(self, period: int):
        # fetch current state in a first place
        workplace = self._get_workplace()
        self._last_state = WorkplaceResources.from_orm(workplace).dict()

        while True:
            await asyncio.sleep(period)
            # if client has gone, no more polling required
            if self._is_alive and not self._is_alive():
                break

            try:
                # WebSocket or DB exception
                updates = self._check_updates()
                if len(updates) and self._callback:
                    await self._callback(updates)
            except Exception as e:
                break   # no handler yet, just break
'''
