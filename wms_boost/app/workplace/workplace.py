from typing import Any, Dict
from app.models import Workplace as DbWorkplace
from app.refunds_dump.today_dump import TodayDump
from werkzeug.utils import cached_property


class Workplace:
    """ Wrap workplace representation in db,
        and fetch related resource from Redis using cache """
    def __init__(self, workplace_in_db: DbWorkplace):
        self._db_state = workplace_in_db

    @cached_property
    def refunds_dump(self) -> TodayDump:
        # return value from redis, use cache
        return TodayDump(self._db_state)

    def __getattr__(self, attr) -> Any:
        # proxy to underlying db state
        return getattr(self._db_state, attr)
