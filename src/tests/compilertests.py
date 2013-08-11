import unittest
import application
from application.compiler import Compiler
from mock import patch, Mock, call

test_input = """
# This is only a test
module normal_module(a=1) {
    translate([1,2,a]) ~arduino-v1(screws=true);
    cube([1,2,3]);
    ~arduino-v1 (screws=false);
    ~circle-v10();
}
normal_module(1);
"""

class CompilerTests(unittest.TestCase):
    def test_compiler_returns_input(self):
        c = Compiler()
        result = c.compile("cube([1,1,1]);")
        self.assertEqual(c.input, "cube([1,1,1]);")
        self.assertEqual(result, "cube([1,1,1]);")
        
    def test_match_tilded_functions(self):
        c = Compiler()
        c.input = test_input
        matches, functions = c.find_seamless_calls()
        self.assertEqual(functions, ["~circle-v10", "~arduino-v1"])
    
    @patch('application.compiler.get_by_uniquename')
    def test_compiler_gets_functions(self, method_mock):
        Compiler().compile(test_input)
        method_mock.assert_has_calls([ call("~circle-v10"), call("~arduino-v1")])
        self.assertEqual(2, method_mock.call_count)
        