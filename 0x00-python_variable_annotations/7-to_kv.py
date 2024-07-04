#!/usr/bin/env python3
"""Module implementing a type-annotated function"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Function taking str and int or float as arguments and returns a
    tuple with the string and and square of the int/float
    """
    return (k, v ** 2)
