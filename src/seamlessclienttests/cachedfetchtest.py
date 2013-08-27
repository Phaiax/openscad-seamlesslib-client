from mock import patch
from seamlessclient import cachedfetch
from seamlessclient.config import Config
import unittest

class CachedFetchTests(unittest.TestCase):
    
    
    def test_uses_cache(self):
        self.assertRaises(cachedfetch.NotFound, cachedfetch.get_by_uniquename, "~abcdefoobar")
        Config().save_module('~abcdefoobar', { 'guid': 'test' }, trigger_write = False)
        mod = cachedfetch.get_by_uniquename("~abcdefoobar")
        self.assertEqual('test', mod['guid'])
        
        
    @patch('seamlessclient.cachedfetch.Config')
    @patch('seamlessclient.cachedfetch.webfetch.get_by_uniquename')
    def test_does_not_cache_unfinished_modules(self, get_by_uniquename, config):
        get_by_uniquename.return_value = { 'finished': False, 'guid' : 'segseg' }
        def e(a):
            raise KeyError
        config().get_module.side_effect = e 
        cachedfetch.get_by_uniquename("segseg")
        self.assertFalse(config().save_module.called)
