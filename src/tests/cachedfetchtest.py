import unittest
from application.config import Config
from application import cachedfetch
import mock

class CachedFetchTests(unittest.TestCase):
    
    
    def test_uses_cache(self):
        self.assertRaises(cachedfetch.NotFound, cachedfetch.get_by_uniquename, "~abcdefoobar")
        Config().save_module('~abcdefoobar', { 'guid': 'test' }, trigger_write = False)
        mod = cachedfetch.get_by_uniquename("~abcdefoobar")
        self.assertEqual('test', mod['guid'])
        
        