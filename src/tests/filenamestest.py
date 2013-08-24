
import unittest
from application.filenames import get_filename_for_compiled_file, has_scad_extension, is_compiled_file, NotAScadFile
from application import compiled_filename_extension, scad_extension

class FilenamesTest(unittest.TestCase):


    def test_generates_compiled_filename(self):
        self.assertEqual("t" + compiled_filename_extension, get_filename_for_compiled_file("t" + scad_extension))
        self.assertRaises(NotAScadFile, get_filename_for_compiled_file, "t")

    def test_has_scad_extension(self):
        self.assertTrue(has_scad_extension("t" + scad_extension))
        self.assertTrue(has_scad_extension("t" + compiled_filename_extension))
        self.assertFalse(has_scad_extension("t.doc"))
        self.assertFalse(has_scad_extension("t"))
        self.assertFalse(has_scad_extension("t.a"))
        self.assertFalse(has_scad_extension("t.docscad"))
        
    def test_is_compiled_file(self):
        self.assertFalse(is_compiled_file("t.doc"))
        self.assertFalse(is_compiled_file("t" + scad_extension))
        self.assertFalse(is_compiled_file("t.a"))
        self.assertFalse(is_compiled_file("t"))
        self.assertTrue(is_compiled_file("t" + compiled_filename_extension))
        
    
        