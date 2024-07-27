#!/usr/bin/env python3
"""Test access_nested_map function using unittest framework"""
import unittest
import requests
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json
from unittest.mock import patch, Mock


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

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, seq, keyerror):
        """Testcase for exception raised by access_nested_map method"""
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, seq)
        self.assertEqual(str(e.exception).strip("'"), keyerror)


class TestGetJson(unittest.TestCase):
    """Class implementing parameterized test cases for get_json function
    from utils module
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, url, payload, get_json_mock):
        """Test case for return value of get_json function"""
        get_json_mock.return_value.json.return_value = payload
        get_json(url)
        get_json_mock.assert_called_once_with(url)
        self.assertEqual(get_json(url), payload)
