#!/usr/bin/env python3
"""
Module implementing a coroutine that calls a function returning a
asyncio.Task
"""
import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Async coroutine that awaits the task_wait_random coroutine and
    returns a list of the delays(float values) from task_wait_random in
    ascending order
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    res = await asyncio.gather(*tasks)
    return sorted(res)
