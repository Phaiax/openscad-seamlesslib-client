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

server_answer_arduino = {
        'guid' : "f90016f9-fc2c-4bf1-9e93-223a3bce0857",
        'modulename' : "my_arduino",
        'description' : "This Module builds an arduino",
        'sourcecode' : "module my_arduino(screws) { }",
        'documentation' : "just call ~arduino-v1",
        'uniquename' : "~arduino-v1",
        'title' : "Arduino",
        'version' : 1 }

server_answer_circle = {
        'guid' : "f90016f9-fc2c-4bf1-9e93-223a3bce0857",
        'modulename' : "draw-circle",
        'description' : "This Module is a kind of stupid",
        'sourcecode' : "module draw-circle(radius = 10) { cylinder(r=radius, h=1); }",
        'documentation' : "just call ~circle-v10",
        'uniquename' : "~circle-v10",
        'title' : "Arduino",
        'version' : 10 }


class CompilerTests(unittest.TestCase):
    def test_compiler_returns_input(self):
        c = Compiler()
        result = c.compile("cube([1,1,1]);")
        self.assertEqual(c.input, "cube([1,1,1]);")
        self.assertEqual(result, "cube([1,1,1]);")
        
    def test_match_tilded_functions(self):
        c = Compiler()
        c.input = test_input
        matches, functions = c.find_calls_to_methods_on_seamless_server()
        self.assertEqual(functions, ["~circle-v10", "~arduino-v1"])
    
    @patch('application.compiler.get_by_uniquename')
    def test_compiler_gets_functions(self, get_by_uniquename_mock):
        get_by_uniquename_mock.side_effect = [server_answer_circle, server_answer_arduino]
        Compiler().compile(test_input)
        get_by_uniquename_mock.assert_has_calls([ call("~circle-v10"), call("~arduino-v1")])
        self.assertEqual(2, get_by_uniquename_mock.call_count)
        
    @patch('application.compiler.Compiler.generate_five_random_chars')
    def test_randomized_names_generation(self, random_mock):
        random_mock.return_value = "abcde"
        c = Compiler()
        c.modules = {"~arduino-v1" : server_answer_arduino,
                     "~circle-v10" : server_answer_circle }
        c.generate_all_randomized_module_names()
        self.assertEqual("arduino-v1-abcde", c.modules['~arduino-v1']['randomized_method_name'])
        self.assertEqual("circle-v10-abcde", c.modules['~circle-v10']['randomized_method_name'])
        
    def test_replacing_orginal_module_name(self):
        module = Compiler().replace_modulename("new_mod_name", "old_mod_name", "module old_mod_name(abc = 13) { }")
        self.assertIn("module new_mod_name(", module)

        module = Compiler().replace_modulename("new_mod_name", "old_mod_name", "module old_mod_name         (abc = 13) { }")
        self.assertIn("module new_mod_name(", module)

        module = Compiler().replace_modulename("new_mod_name", "old_mod_name", "module       old_mod_name(abc = 13) { }")
        self.assertIn("module new_mod_name(", module)

        module = Compiler().replace_modulename("new_mod_name", "old_mod_name", """
                        module 
                        old_mod_name(abc = 13) { 
                                module old_mod_name_2() { } 
                                old_mod_name_2();
                                old_mod_name();
                        }""")
        self.assertIn("module new_mod_name(", module)
        self.assertIn("module old_mod_name_2(", module) # do not delete anything
        self.assertIn("old_mod_name_2();", module)
        self.assertIn("old_mod_name();", module)

    def test_get_5_random_chars(self):
        r = Compiler().generate_five_random_chars()
        r2 = Compiler().generate_five_random_chars()
        self.assertNotEqual(r, r2)
        self.assertEqual(5, len(r))

    @patch('application.compiler.Compiler.generate_five_random_chars')
    def test_randomize_module_name(self, generate_five_random_chars_mock):
        generate_five_random_chars_mock.return_value = "abcde"
        self.assertEqual("circle-v1-abcde", Compiler().randomize_module_name("circle-v1"))
        
    @patch('application.compiler.Compiler.generate_five_random_chars')
    @patch('application.compiler.get_by_uniquename')
    def test_compiler_inserts_functions_to_end_of_file_and_strips_tilde(self, get_by_uniquename_mock, random_mock):
        get_by_uniquename_mock.side_effect = [server_answer_circle, server_answer_arduino]
        random_mock.return_value = "abcde"
        result = Compiler().compile(test_input)
        self.assertIn("module arduino-v1-abcde(screws)", result)
        self.assertIn("module circle-v10-abcde(", result)
        
    @patch('application.compiler.Compiler.generate_five_random_chars')
    @patch('application.compiler.get_by_uniquename')
    def test_compiler_replaces_uniquename_in_module_calls_with_randomized_name(self, get_by_uniquename_mock, random_mock):
        get_by_uniquename_mock.side_effect = [server_answer_circle, server_answer_arduino]
        random_mock.return_value = "abcde"
        result = Compiler().compile(test_input)
        self.assertIn("circle-v10-abcde();", result)
        self.assertIn("arduino-v1-abcde (screws=false);", result)
        self.assertIn("arduino-v1-abcde(screws=true);", result)
        
        
        