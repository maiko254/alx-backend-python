#!/usr/bin/env python3
"""Module measuring the runtime of an async coroutine"""
import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Function taking integers n and max_delays as args and measures the total
    runtime for coroutine wait_n(n, max_delay), and returns the average
    runtime per coroutine float
    """
    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    total_time = time.perf_counter() - start
    return total_time / n
