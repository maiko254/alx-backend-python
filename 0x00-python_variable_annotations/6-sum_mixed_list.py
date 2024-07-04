#!/usr/bin/env python3
"""Module implementing type-annotated function"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Function taking a list of floats and integers and returning their sum
    as float
    """
    return sum(mxd_lst)
