#!/usr/bin/env python3
""" Test module for GithubOrgClient class """
import unittest
import client
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


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


    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("clickdigital", {"repos_url": "https://api.github.com/orgs/clickdigital/repos"})
        ])
    def test_public_repos_url(self, org_name, expected_value):
        """Tests return value of _public_repos_url method"""
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = expected_value
            client = GithubOrgClient(org_name)
            result = client._public_repos_url
            self.assertEqual(result, f"https://api.github.com/orgs/{org_name}/repos")
