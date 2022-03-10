from typing import Any
from app.models import Workplace
from app.utils.client_time import ClientTime
from app.redis import REDIS_POOL
import redis


# helper
def _get_next_midnight(client_time: ClientTime) -> int:
    pass


class TodayDump:
    """ Wrap LastRefundsDump from db in order to provide
        access to its up-to-date values (both from db and Redis) """
    def __init__(self, workplace: Workplace):
        self._client_time = ClientTime(workplace)
        self._redis_conn = redis.Redis(connection_pool=REDIS_POOL)

        last_dump = workplace.last_refunds_dump

        self._workplace_id = last_dump.workplace_id
        self._id = last_dump.id
        self._report_url = last_dump.report_url
        self._redis_key = last_dump.redis_key
        # just placeholders for redis values
        self._included = None
        self._processed = None
        self._status = None

        self._init_from_redis(self, self._redis_key)


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
        self._update_redis_values(('included', self._included))


    def update_progress(self, processed: int) -> None:
        # update `processed` field and write out changes to Redis
        self._processed = processed
        values = [('processed', processed)]
        if self._processed == self.included:
            values.append(('status', 'completed'))
        self._update_redis_values(values)


    def _update_redis_values(*args) -> None:
        new_state = {
            k : v
                for k, v in args
        }
        r = self._redis_conn
        r.hmset(self._redis_key, new_state)
        r.expireat(
                self._redis_key,
                _get_next_midnight())


    def _init_from_redis(self, redis_key: str) -> None:
        r = self._redis_conn
        # check existance/expiration
        if not r.exists(redis_key) or r.pttl(redis_key) <= 0:
            # set default values if key has expired or not exists
            included = 0
            processed = 0
            status = "default"
        else:
            # use redis values otherwise
            state_dict = r.hgetall(redis_key)
            included = state_dict['included']
            processed = state_dict['processed']
            status = state_dict['status']

        self._included = included
        self._processed = processed
        self._status = status
