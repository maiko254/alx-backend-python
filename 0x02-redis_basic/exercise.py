#!/usr/bin/env python3
"""Module implementing a redis cache"""
import redis
import uuid
from typing import Union


class Cache:
    """Cache class for storing data in redis"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Type-annotated function storing data in redis and returning a key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
