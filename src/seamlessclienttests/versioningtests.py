from mock import patch
from seamlessclient import get_client_version
from seamlessclient.config import Config
from seamlessclient.version import get_server_version_info, \
    is_this_client_supported, is_most_recent_version, server_version_cache, \
    UnsupportedVersion, raise_if_unsupported, WrongServer
from seamlessclient.webfetch import run_server_request
import unittest

class VersioningTests(unittest.TestCase):
    def test_has_version(self):
        self.assertTrue(get_client_version() > 0)
        self.assertTrue(get_client_version() < 100000)
        
        
        
    def test_can_check_server_version(self):
        server_version_info = get_server_version_info()
        self.assertTrue(server_version_info['server_version'] > 0)
        self.assertTrue(server_version_info['server_version'] < 1000)
        self.assertTrue(server_version_info['min_supported_client'] > 0)
        self.assertTrue(server_version_info['min_supported_client'] < 1000)
        self.assertTrue(server_version_info['most_recent_client_version'] > 0)
        self.assertTrue(server_version_info['most_recent_client_version'] < 1000)
        
    @patch('seamlessclient.version.run_server_request')
    def test_server_request_is_cached(self, run_server_request):
        server_version_cache.clear()
        run_server_request.return_value = { 'key': 'val'}
        get_server_version_info()
        get_server_version_info()
        self.assertEqual(1, run_server_request.call_count)
        server_version_cache.clear()

        
    @patch('seamlessclient.version.get_server_version_info')
    @patch('seamlessclient.version.get_client_version')
    def test_can_check_if_supported(self, get_client_version, get_server_version_info):
        get_server_version_info.return_value = { "server_version" : 2,
               "min_supported_client" : 2,
               "most_recent_client_version": 4 }
        get_client_version.side_effect = [1, 2, 3, 4, 5]
        self.assertFalse(is_this_client_supported())
        self.assertTrue(is_this_client_supported())
        self.assertTrue(is_this_client_supported())
        self.assertTrue(is_this_client_supported())
        self.assertFalse(is_this_client_supported())
        
    @patch('seamlessclient.version.is_this_client_supported')
    def test_raise_if_unsupported(self, is_this_client_supported):
        is_this_client_supported.return_value = False
        self.assertRaises(UnsupportedVersion, raise_if_unsupported)
        
    @patch('seamlessclient.version.get_server_version_info')
    @patch('seamlessclient.version.get_client_version')
    def test_can_check_if_most_recent_version(self, get_client_version, get_server_version_info):
        get_server_version_info.return_value = { "server_version" : 2,
               "min_supported_client" : 2,
               "most_recent_client_version": 4 }
        get_client_version.side_effect = [1, 2, 3, 4, 5]
        self.assertFalse(is_most_recent_version())
        self.assertFalse(is_most_recent_version())
        self.assertFalse(is_most_recent_version())
        self.assertTrue(is_most_recent_version())
        self.assertTrue(is_most_recent_version())
    
    @patch('seamlessclient.webfetch.Config')
    def test_raises_if_wrong_server(self, config):
        config().get_server.return_value = "google.de"
        server_version_cache.clear()
        self.assertRaises(WrongServer, raise_if_unsupported)
        