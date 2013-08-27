from seamlessclient.config import Config
import seamlessclient
import unittest

class ConfigTests(unittest.TestCase):
    def test_can_save_value(self):
        Config().save('test', '1234')
        self.assertEqual('1234', Config().get('test', 'empty'))

    def test_return_default_if_not_existent(self):
        self.assertEqual('default', Config().get('foooooo', 'default'))
        
    def test_can_clear_config(self):
        Config().save('test', '1234')
        Config().clear()
        self.assertEqual('default', Config().get('test', 'default'))

    def test_get_default_server(self):
        Config().clear()
        self.assertEqual(Config().get_server(), seamlessclient.default_servers[0])
        
    def test_can_set_server(self):
        from seamlessclient.version import server_version_cache
        server_version_cache.update({'23': '234'})
        Config().clear()
        Config().set_server("test.de")
        self.assertEqual({}, server_version_cache)
        self.assertEqual(Config().get_server(), "test.de")
        
    def test_can_store_module_dict(self):
        Config().clear()
        Config().save_module('~px-test-v1', {'a name': 'a value'})
        self.assertEqual(Config().get_module('~px-test-v1')['a name'], 'a value')
        
    def test_can_have_reserverd_names(self):
        Config().set_server("test.de")
        Config().save_module('server', {'a name': 'a value'})
        self.assertEqual(Config().get_server(), "test.de")
        
        