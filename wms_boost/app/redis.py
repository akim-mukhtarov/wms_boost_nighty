import redis


_PORT = 6379

REDIS_POOL = redis.ConnectionPool(host='10.0.0.1', port=_PORT, db=0)
