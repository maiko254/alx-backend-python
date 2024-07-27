#!/usr/bin/env python3
"""Test access_nested_map function using unittest framework"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Class implementing parametrized testing for access_nested_map method"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, seq, expected):
        """Testcase for return value of access_nested_map method"""
        self.assertEqual(access_nested_map(nested_map, seq), expected)
