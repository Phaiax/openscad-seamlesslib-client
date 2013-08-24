import unittest
from seamlessclient import webfetch

class FetchTests(unittest.TestCase):
    def test_request_fails_with_invalid_name(self):
        self.assertRaises(webfetch.NotFound, webfetch.get_by_uniquename, "foo")
     
    def test_raw_request_returns_jsonable_object(self):
        test1 = webfetch.get_by_uniquename("~px-test-v1")
        self.assertEqual(test1['guid'], "f90016f9-fc2c-4bf1-9e93-223a3bce0857")
        self.assertEqual(test1['modulename'], "test")
        self.assertEqual(test1['description'], "Desc")
        self.assertEqual(test1['sourcecode'], "module test(")
        self.assertEqual(test1['documentation'], "Dok")
        self.assertEqual(test1['uniquename'], "~px-test-v1")
        self.assertEqual(test1['title'], "LatestMod")
        self.assertEqual(test1['version'], 1)
    
    def test_url_generation(self):
        self.assertEqual(webfetch.make_url("localhost", "get_by_uniquename", "ab-13"), "http://localhost/api/get_by_uniquename/ab-13/")
        self.assertEqual(webfetch.make_url("http://lo", "fkt", "ab-13"), "http://lo/api/fkt/ab-13/")
        self.assertEqual(webfetch.make_url("http://lo/", "fkt", "ab-13"), "http://lo/api/fkt/ab-13/")
        self.assertEqual(webfetch.make_url("http://lo:8000", "fkt", "ab-13"), "http://lo:8000/api/fkt/ab-13/")
        self.assertEqual(webfetch.make_url("lo:8000", "fkt", "ab-13"), "http://lo:8000/api/fkt/ab-13/")
        self.assertEqual(webfetch.make_url("lo/", "fkt", "ab-13"), "http://lo/api/fkt/ab-13/")
        
    def test_user_url_generation(self):
        self.assertEqual(webfetch.make_user_url("localhost", "dbbd92b1-df0b-459e-a5c9-27ea43b2cab4"), "http://localhost/show/dbbd92b1-df0b-459e-a5c9-27ea43b2cab4/")
        self.assertEqual(webfetch.make_user_url("http://localhost", "dbbd92b1-df0b-459e-a5c9-27ea43b2cab4"), "http://localhost/show/dbbd92b1-df0b-459e-a5c9-27ea43b2cab4/")
        self.assertEqual(webfetch.make_user_url("http://localhost/", "dbbd92b1-df0b-459e-a5c9-27ea43b2cab4"), "http://localhost/show/dbbd92b1-df0b-459e-a5c9-27ea43b2cab4/")
        self.assertEqual(webfetch.make_user_url("localhost/", "dbbd92b1-df0b-459e-a5c9-27ea43b2cab4"), "http://localhost/show/dbbd92b1-df0b-459e-a5c9-27ea43b2cab4/")

