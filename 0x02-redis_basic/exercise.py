#!/usr/bin/env python3
"A module for utilizing the Redis NoSQL data storage"

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """Initialize a new cache object."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        "Stores a value in Redis and returns the corresponding key."
        k = str(uuid.uuid4())
        self._redis.set(k, data)
        return k
