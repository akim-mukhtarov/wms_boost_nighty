from app.models import LastRefundsDump
from typing import Any


class LastDump:
    """ Wrap `LastRefundsDump`, stored in db in order
        to provide up-to-date state """
    def __init__(self, last_dump_in_db: LastRefundsDump):
        self._stored_state = last_dump_in_db
        self._is_up_to_date = None  # used for cache

    @property
    def included(self) -> int:
        return self._get_actual_included()

    @property
    def status(self) -> LastRefundsDump.status_choices:
        return self._get_actual_status()

    def add_items(self, just_included: int) -> None:
        if self.is_up_to_date():
            self._stored_state.included += just_included
        else:
            self._stored_state.included = just_included

    def _get_actual_included(self) -> int:
        if self.is_up_to_date():
            return self._stored_state.included
        else:
            return 0

    def _get_actual_status(self) -> LastRefundsDump.status_choices:
        if self.is_up_to_date():
            return self._stored_state.status
        else:
            return LastRefundsDump.status_choices.default

    def is_up_to_date(self) -> bool:
        """ Cached version of underlying model' `is_up_to_date` method """
        if self._is_up_to_date is not None:
            return self._stored_state.is_up_to_date()
        else:
            return self._is_up_to_date

    def __getattr__(self, attr: str) -> Any:
        # used to delegate getters to underlying model's state
        return getattr(self._stored_state, attr)
