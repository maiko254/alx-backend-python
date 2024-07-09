#!/usr/bin/env python3
"""Module that measures the total runtime of a coroutine"""
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Coroutine that executes async_comprehension four times in parallel and
    returns the total runtime
    """
    start_time = time.perf_counter()
    await asyncio.gather(async_comprehension(), async_comprehension(),
                         async_comprehension(), async_comprehension())
    total_time = time.perf_counter() - start_time

    return total_time
