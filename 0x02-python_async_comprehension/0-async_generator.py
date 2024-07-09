#!/usr/bin/env python3
"""Module implementing an asynchronous generator"""
import asyncio
from typing import Generator
import random


async def async_generator() -> Generator[float, None, None]:
    """
    Coroutine looping 10 times and each time asynchronously waiting for 1
    second then yielding a random value between 0 and 10
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
