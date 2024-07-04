#!/usr/bin/env python3
"Module implementing a type-annotated function"
from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    Function taking a list of floats as argument and returns their sum as
    float
    """
    return sum(input_list)
