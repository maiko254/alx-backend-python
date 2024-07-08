#!/usr/bin/env python3
"""Module creating an asynchronous coroutine"""
import asyncio
import random
import time


async def wait_random(max_delay: int = 10) -> float:
    """
    Async coroutine taking an integer max_delay and waits for a random
    delay between 0 and max_delay then returns it
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
