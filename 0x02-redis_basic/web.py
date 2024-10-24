#!/usr/bin/env python3
"""
Web cache and tracker module
"""
import redis
import requests
from functools import wraps
from typing import Callable


def cache_with_expiry(expiration_time: int = 10) -> Callable:
    "Decorator to cache the HTML content of a page for 10 seconds."
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client = redis.Redis()
            cache_key = f"cached:{url}"
            count_key = f"count:{url}"
            redis_client.incr(count_key)
            cached_content = redis_client.get(cache_key)
            if cached_content:
                return cached_content.decode('utf-8')
            content = func(url)
            redis_client.setex(cache_key, expiration_time, content)
            
            return content
        return wrapper
    return decorator


@cache_with_expiry()
def get_page(url: str) -> str:
    "Fetches the HTML content of the given URL."
    response = requests.get(url)
    response.raise_for_status()
    return response.text
