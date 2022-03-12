from typing import Any, Dict
from app.models import Workplace
from app.utils.client_time import ClientTime
from app.redis import REDIS_POOL
import redis


# helper
def _get_next_midnight(timezone_name: str) -> int:
    client_time = ClientTime(timezone_name)
    next_midnight = client_time.days_diff(1)
    return next_midnight.timestamp()


class TodayDump:
    """ Wrap const params from DB and mutable values from Redis """

    _default_state = {
        'included': 0,
        'processed': 0,
        'status': 'default'
    }

    def __init__(self, workplace: Workplace):
        self._redis_conn = redis.Redis(connection_pool=REDIS_POOL)

        last_dump = workplace.refunds_dump_settings

        self._id = last_dump.id
        self._workplace_id = last_dump.workplace_id
        self._report_url = last_dump.report_url
        self._redis_key = last_dump.redis_key
        self._timezone = workplace.timezone

        state = self._get_state(self._redis_conn, self._redis_key)
        self._included = state['included']
        self._processed = state['processed']
        self._status = state['status']
        self._state_dict = state

    @property
    def id(self) -> int:
        return self._id

    @property
    def workplace_id(self) -> int:
        return self._workplace_id

    @property
    def report_url(self) -> str:
        return self._report_url

    @property
    def included(self) -> int:
        return self._included

    @property
    def processed(self) -> int:
        return self._processed

    @property
    def status(self) -> str:
        return self._status

    def add_new(self, just_included: int) -> None:
        # supposed to be used by `dump_refunds` functio
        # update `included` field and write out changes to Redis
        self._included += just_included
        self._update_state(('included', self._included))

    def update_progress(self, processed: int) -> None:
        # update `processed` field and write out changes to Redis
        self._processed = processed
        values = [('processed', processed)]
        if self._processed == self.included:
            values.append(('status', 'completed'))
        self._update_state(values)

    def _update_state(self, *args) -> None:
        """ Update/set values stored in Redis
            setup expiration date to the end of the current day """
        for k, v in args:
            self._state_dict[k] = v

        r = self._redis_conn
        r.hmset(self._redis_key, self._state_dict)
        r.expireat(
                self._redis_key,
                _get_next_midnight(self._timezone))

    @classmethod
    def _get_state(cls, r: redis.Redis, redis_key: str) -> Dict:
        """ Get values from Redis, if key exists.
            Return default otherwise """
        if not r.exists(redis_key) or r.pttl(redis_key) <= 0:
            return cls._default_state
        else:
            return r.hgetall(redis_key)
