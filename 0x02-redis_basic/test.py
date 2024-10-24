#!/usr/bin/env python3
"A module for utilizing the Redis NoSQL data storage"

import redis
import uuid
from typing import Union, Callable
from functools import wraps  # إضافة الاستيراد هنا

def count_calls(method: Callable) -> Callable:
    "Counts the calls made to a method within the Cache class."
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        "Delivers the given method after updating its call counter."
        k = method.__qualname__
        c = self._redis.incr(k)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    def __init__(self):
        """Initialize a new cache object."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        "Stores a value in Redis and returns the corresponding key."
        k = str(uuid.uuid4())
        self._redis.set(k, data)
        return k

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        "Gets a value from the Redis data storage"
        d = self._redis.get(key)
        if d is None:
            return None  # إرجاع None إذا كان المفتاح غير موجود
        if fn:
            return fn(d)
        return d

    def get_str(self, key: str) -> str:
        """Changes bytes into a string."""
        return self.get(key, fn=lambda d: d.decode('utf-8') if d else None)

    def get_int(self, key: str) -> int:
        """Gets an integer value stored in Redis."""
        return self.get(key, fn=lambda d: int(d) if d else None)

