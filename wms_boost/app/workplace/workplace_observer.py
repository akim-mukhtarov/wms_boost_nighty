from __future__ import annotations
from typing import TypeVar, Optional, Callable, Dict, Awaitable
from fastapi import WebSocket
import asyncio
import pydantic



class WorkplaceResources(pydantic.BaseModel):

    class RefundsDump:
        def __init__(self, models.LastRefundsDump):
            pass

    class StorageSteps:
        def __init__(self, models.StorageSteps):
            pass

    last_refunds_dump: RefundsDump
    storage_steps: StorageSteps

    class Config:
        orm_mode=True


OptionalCallback = TypeVar('OptionalCallback', bind=Optional[Callable])
AsyncCallback = TypeVar('AsyncCallback', bind=Callable[[Dict], Awaitable[None]])

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

    def _check_updates(self):
        workplace = self._get_workplace()
        state_dict = WorkplaceResources(workplace).dict()
        # just a dict of changes
        diff = {
            k : v
                for k, v in (
                    (k, state_dict[k])
                        for k in self._state
                            if state_dict[k] != self._state[k]
                )
        }
        return diff


    async def poll(period: int):
        while True:
            # if client has gone, no more polling required
            if self._is_alive and not self._is_alive():
                break

            try:
                # WebSocket or DB exception
                updates = self._check_updates()
                if len(updates) and self._callback:
                    await self._callback(updates)
            except Exception:
                break

            await asyncio.sleep(period)
