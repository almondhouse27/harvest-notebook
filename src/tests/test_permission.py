import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import unittest
from unittest.mock import patch, Mock
from permission import robot_handshake

class TestRobotHanshakeDoesNotResultInDeath(unittest.TestCase):

    @patch('permission.requests.get')
    @patch('permission.random.choice')
    def test_permission_granted(self, mock_random_choice, mock_get):
        url = "https://example.com/some-page"
        user_agents = ["Agent1", "Agent2"]
        proxies = ["proxy1", "proxy2"]
        timeout = 5
        delay = 0
        mock_random_choice.side_effect = lambda x: x[0]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "User-agent: *\nAllow: /"
        mock_get.return_value = mock_response
        result = robot_handshake(url, user_agents, timeout, proxies, delay)
        self.assertTrue(result)
        mock_get.assert_called_once()

    @patch('permission.requests.get')
    @patch('permission.random.choice')
    def test_permission_denied(self, mock_random_choice, mock_get):
        url = "https://example.com/forbidden"
        user_agents = ["Agent1", "Agent2"]
        proxies = None
        timeout = 5
        delay = 0
        mock_random_choice.side_effect = lambda x: x[0]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "User-agent: *\nDisallow: /forbidden"
        mock_get.return_value = mock_response
        result = robot_handshake(url, user_agents, timeout, proxies, delay)
        self.assertFalse(result)
        mock_get.assert_called_once()

    @patch('permission.requests.get')
    @patch('permission.random.choice')
    def test_robots_txt_not_found(self, mock_random_choice, mock_get):
        url = "https://example.com/no-robots"
        user_agents = ["Agent1"]
        proxies = None
        timeout = 5
        delay = 0
        mock_random_choice.side_effect = lambda x: x[0]
        mock_get.side_effect = Exception("404 Not Found")
        result = robot_handshake(url, user_agents, timeout, proxies, delay)
        self.assertFalse(result)

    @patch('permission.requests.get')
    def test_invalid_url(self, mock_get):
        url = "invalid-url"
        user_agents = ["Agent1"]
        proxies = None
        timeout = 5
        delay = 0
        result = robot_handshake(url, user_agents, timeout, proxies, delay)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()