#!/usr/bin/env python3
""" Test module for GithubOrgClient class """
import unittest
import client
from unittest.mock import patch, Mock, PropertyMock, MagicMock
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

    def test_public_repos_url(self) -> None:
        """Tests return value of `_public_repos_url` property"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get: MagicMock) -> None:
        """test case for return value of public_repos method/property"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos",
            "repos": [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "html_url": "https://github.com/google/episodes.dart",
                    "description": "A framework for timing performance of web apps.",
                    "fork": False,
                },
                {
                    "id": 7776515,
                    "name": "cpp-netlib",
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "html_url": "https://github.com/google/cpp-netlib",
                    "fork": True,
                }
            ]
        }
        mock_get.return_value = test_payload["repos"]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_repos:
            mock_repos.return_value = test_payload["repos_url"]
            result = GithubOrgClient("google").public_repos()
            expected_result = [
                        "episodes.dart",
                        "cpp-netlib"
                    ]
            self.assertEqual(result, expected_result)
            mock_repos.assert_called_once()
            mock_get.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "apache-2.0"}}, "apache-2.0", True),
        ({"license": {"key": "apache-1.0"}}, "apache-2.0", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        result = GithubOrgClient("google").has_license(repo, license_key)
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
