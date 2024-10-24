#!/usr/bin/env python3
"A module for utilizing the Redis NoSQL data storage"

import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    "Counts the calls made to a method within the Cache class."
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        "Delivers the given method after updating its call counter."
        k = method.__qualname__
        c = self._redis.incr(k)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    "Stores the history of inputs and outputs for a particular function."
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        "Wraps the method and tracks its arguments in Redis."
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, result)
        return result
    return wrapper


class Cache:
    def __init__(self):
        """Initialize a new cache object."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        "Stores a value in Redis and returns the corresponding key."
        k = str(uuid.uuid4())
        self._redis.set(k, data)
        return k

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        "Gets a value from the Redis data storage"
        d = self._redis.get(key)
        if d is None:
            return None
        if fn:
            return fn(d)
        return d

    def get_str(self, key: str) -> str:
        """Changes bytes into a string."""
        return self.get(key, fn=lambda d: d.decode('utf-8') if d else None)

    def get_int(self, key: str) -> int:
        """Gets an integer value stored in Redis."""
        return self.get(key, fn=lambda d: int(d) if d else None)

    def replay(self, method: Callable) -> None:
        "Displays the history of calls for the specified method."
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)
        call_count = self._redis.get(method.__qualname__).decode('utf-8')
        print(f"{method.__qualname__} was called {call_count} times:")
        for input_data, output_data in zip(inputs, outputs):
            print(f"{method.__qualname__}(*{input_data.decode('utf-8')}) -> "
                  f"{output_data.decode('utf-8')}")
