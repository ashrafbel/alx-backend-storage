#!/usr/bin/env python3
"Module to fetch and cache web pages using Redis."

import requests
import redis
from functools import wraps
from typing import Callable


cache = redis.Redis()


def count_accesses(method: Callable) -> Callable:
    "Decorator to count accesses to the given URL."
    @wraps(method)
    def wrapper(url: str) -> str:
        cache.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_page(method: Callable) -> Callable:
    "Decorator to cache the HTML content of a page for 10 seconds."
    @wraps(method)
    def wrapper(url: str) -> str:
        cached_content = cache.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode('utf-8')
        content = method(url)
        cache.setex(f"cached:{url}", 10, content)
        return content
    return wrapper


@count_accesses
@cache_page
def get_page(url: str) -> str:
    "Fetches the HTML content of the given URL."
    response = requests.get(url)
    return response.text
