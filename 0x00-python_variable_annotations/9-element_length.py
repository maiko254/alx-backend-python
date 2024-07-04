#!/usr/bin/env python3
"""Module with a type-annotated function"""
from typing import Iterable, List, Tuple, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Function taking an iterable as argument and returning a list of tuples with
    a sequence and integer as elements of the tuple
    """
    return [(i, len(i)) for i in lst]
