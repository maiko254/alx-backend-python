#!/usr/bin/env python3
""" Test module for GithubOrgClient class """
import unittest
from unittest.mock import patch
from parameterized import parameterized
GithubOrgClient = __import__('client').GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ Test cases for methods in GithubOrgClient class """
    @parameterized.expand([
        ('google', {"name": "google"}),
        ('abc', {"name": "abc"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_value, get_json_mock):
        """ Test case for return value of org method in GithubOrgClient class
        """
        get_json_mock.return_value = expected_value
        client = GithubOrgClient(org_name)
        result = client.org
        url = f"https://api.github.com/orgs/{org_name}"
        get_json_mock.assert_called_once_with(url)
        self.assertEqual(result, expected_value)
