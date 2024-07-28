#!/usr/bin/env python3
""" Test module for GithubOrgClient class """
import unittest
import client
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError


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
        ("click", {"repos_url": "https://api.github.com/orgs/click/repos"})
        ])
    def test_public_repos_url(self, org_name, expected_value):
        """Tests return value of _public_repos_url method"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = expected_value
            client = GithubOrgClient(org_name)
            result = client._public_repos_url
            self.assertEqual(result,
                             f"https://api.github.com/orgs/{org_name}/repos")

    @parameterized.expand([
        ("https://api.github.com/orgs/google/repos", [{"name": "truth"}])
    ])
    @patch('client.get_json')
    def test_public_repos(self, url, public_repo, mock_get):
        """test case for return value of public_repos method/property"""
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_repos:
            mock_repos.return_value = url
            mock_get.return_value = public_repo
            client = GithubOrgClient("google")
            result = client.public_repos()
            expected_result = ["truth"]
            mock_repos.assert_called_once()
            mock_get.assert_called_once()
            self.assertEqual(result, expected_result)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False)
    ])
    @patch('client.GithubOrgClient.has_license')
    def test_has_license(self, repo, license_key, expected, mock_has_license):
        """Test has_license method"""
        mock_has_license.return_value = expected
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level mocks"""
        cls.get_patcher = patch('requests.get',
                                side_effect=cls.get_json_side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def get_json_side_effect(cls, url):
        """Side effect function for requests.get().json()"""
        mock_response = Mock()
        if 'orgs/google' in url:
            mock_response.json.return_value = cls.org_payload
        if 'orgs/google/repos' in url:
            mock_response.json.return_value = cls.repos_payload
        return mock_response

    def test_public_repos(self):
        """Test public_repos method returns the expected repos"""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method returns repos with Apache license"""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos('apache-2.0'), self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """Tear down class-level mocks"""
        cls.get_patcher.stop()
