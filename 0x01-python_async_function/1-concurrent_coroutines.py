#!/usr/bin/env python3
"""Module implementing multiple coroutines"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Async coroutine that awaits the coroutine wait_random and
    returns a list of the delays(float values) from wait_random in ascending
    order
    """
    tasks = [wait_random(max_delay) for _ in range(n)]
    res = await asyncio.gather(*tasks)
    return sorted(res)
