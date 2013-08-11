import unittest
from application.config import Config
import application

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
        self.assertEqual(Config().get_server(), application.default_servers[0])
        
    def test_can_set_server(self):
        Config().clear()
        Config().set_server("test.de")
        self.assertEqual(Config().get_server(), "test.de")
        
    def test_can_store_module_dict(self):
        Config().clear()
        Config().save_module('~px-test-v1', {'a name': 'a value'})
        self.assertEqual(Config().get_module('~px-test-v1')['a name'], 'a value')
        
    def test_can_have_reserverd_names(self):
        Config().set_server("test.de")
        Config().save_module('server', {'a name': 'a value'})
        self.assertEqual(Config().get_server(), "test.de")
        
        