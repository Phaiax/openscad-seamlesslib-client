import unittest
import os
import shutil
import time
from seamlessclient.filesystemwatcher import Watcher
from mock import MagicMock, call
from seamlessclient import compiled_filename_extension, scad_extension, test_path

class FolderWatcherTests(unittest.TestCase):

    # Should watch all .scad files
    # excluding .compiled.scad
    # Should return a flag, if the .compiled.scad file exists next to the .scad file
    # Should call a given method if a change is detected

    ignore_this_testcase = True

    def setUp(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        unittest.TestCase.setUp(self)
        self.test_path = test_path
        self.create_test_folder_structure()
        self.w = Watcher(self.test_path)
        
    def create_test_folder_structure(self):
        self.delete_test_folder_if_exists()
        os.makedirs(self.test_path)
        os.makedirs(os.path.join(self.test_path, "folder1"))
        # os.makedirs(os.path.join(self.test_path, "folder2"))
        open(os.path.join(self.test_path, "file0" + scad_extension), 'a').close()
        # open(os.path.join(self.test_path, "folder1", "file1" + scad_extension), 'a').close()
        
    def delete_test_folder_if_exists(self):
        if os.path.exists(self.test_path):
            shutil.rmtree(self.test_path)
        
    def tearDown(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        unittest.TestCase.tearDown(self)
        self.delete_test_folder_if_exists()
        
    def test_can_catch_file_creations(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        self.w.start()
        path = os.path.join(self.test_path, "file55" + scad_extension)
        open(path, 'a').close()
        time.sleep(0.3)
        self.w.stop()
        time.sleep(0.3)
        self.assertIn([path, False], self.w.changed_files)
        self.assertEqual(1, len(self.w.changed_files))
            
    def test_calls_handler(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        m = MagicMock()
        self.w.start()
        self.w.set_handler(m)
        path = os.path.join(self.test_path, "file55" + scad_extension)
        open(path, 'a').close()
        time.sleep(0.3)
        self.w.stop()
        time.sleep(0.3)
        self.assertEquals(call(path, False), m.call_args)
               
    def test_can_catch_file_modifications(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        self.w.start()
        path = os.path.join(self.test_path, "file0" + scad_extension)
        file = open(path, 'a')
        file.write("test")
        file.close()
        time.sleep(0.3)
        self.w.stop()
        time.sleep(0.3)
        self.assertIn([path, False], self.w.changed_files)
        self.assertEqual(1, len(self.w.changed_files))
        
    def test_can_catch_file_movements(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        self.w.start()
        path = os.path.join(self.test_path, "file0" + scad_extension)
        path_new = os.path.join(self.test_path, "file2" + scad_extension)
        os.rename(path, path_new)
        self.w.stop()
        time.sleep(0.5)
        self.assertIn([path_new, False], self.w.changed_files)
        self.assertEqual(1, len(self.w.changed_files))
  
    def test_can_catch_files_in_subfolders(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        self.w.start()
        path = os.path.join(self.test_path, "folder1", "file55" + scad_extension)
        open(path, 'a').close()
        time.sleep(0.3)
        self.w.stop()
        time.sleep(0.3)
        self.assertIn([path, False], self.w.changed_files)
        self.assertEqual(1, len(self.w.changed_files))
    
    def test_ignores_folder_creations(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        self.w.start()
        os.makedirs(os.path.join(self.test_path, "folder3"))
        time.sleep(0.3)
        self.w.stop()
        time.sleep(0.3)
        self.assertEqual(0, len(self.w.changed_files))
        
    def test_only_watches_pscad_files(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        self.w.start()
        path = os.path.join(self.test_path, "folder1", "file55.some")
        open(path, 'a').close()
        time.sleep(0.3)
        self.w.stop()
        time.sleep(0.3)
        self.assertEqual(0, len(self.w.changed_files))
        
        self.w.start()
        path = os.path.join(self.test_path, "folder1", "file55" + compiled_filename_extension)
        open(path, 'a').close()
        time.sleep(0.3)
        self.w.stop()
        time.sleep(0.3)
        self.assertEqual(0, len(self.w.changed_files))

    def test_returns_flag_if_compiled_file_exists(self):
        if FolderWatcherTests.ignore_this_testcase:
            return
        # Create compiled file
        open(os.path.join(self.test_path, "file0" + compiled_filename_extension), 'a').close()
        self.w.start()
        path = os.path.join(self.test_path, "file0" + scad_extension)
        file = open(path, 'a')
        file.write("test")
        file.close()
        time.sleep(0.3)
        self.w.stop()
        time.sleep(0.3)
        self.assertIn([path, True], self.w.changed_files)
        self.assertEqual(1, len(self.w.changed_files))
        
