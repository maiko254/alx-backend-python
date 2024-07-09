#!/usr/bin/env python3
"""
Module implementing a coroutine that uses asynchronous comprehension to
loop over another coroutine
"""
import asyncio
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Coroutine using async comprehensing over async_generaor coroutine to
    collect and return 10 random numbers
    """
    res = [i async for i in async_generator()]
    return res
