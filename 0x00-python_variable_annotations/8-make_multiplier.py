#!/usr/bin/env python3
"""Module implementing a type-annotated function returning another function"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Function that takes a float multiplier as argument and returns
    a function that multiplies a float by multiplier
    """
    def multiply(value: float) -> float:
        return value * multiplier
    return multiply
