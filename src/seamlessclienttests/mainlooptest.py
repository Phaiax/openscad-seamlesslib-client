from seamlessclient import compiled_filename_extension, scad_extension, test_path, \
    mainloop
from seamlessclient.compiler import Compiler
from seamlessclient.filenames import get_filename_for_compiled_file
from mock import patch
from seamlessclienttests.compilertests import test_input, server_answer_arduino, \
    server_answer_circle
import os
import shutil
import threading
import time
import unittest

class MainLoopTests(unittest.TestCase):
    
    ignore_this_testcase = False

    def setUp(self):
        if MainLoopTests.ignore_this_testcase:
            return
        unittest.TestCase.setUp(self)
        self.create_test_folder_structure()
        mainloop.instance = None
        mainloop.instance = mainloop.MainLoop()
        
    def create_test_folder_structure(self):
        self.delete_test_folder_if_exists()
        os.makedirs(test_path)
        
    def delete_test_folder_if_exists(self):
        if os.path.exists(test_path):
            shutil.rmtree(test_path)
        
    def tearDown(self):
        if MainLoopTests.ignore_this_testcase:
            return
        unittest.TestCase.tearDown(self)
        #self.delete_test_folder_if_exists()
  
    
    
    @patch('seamlessclient.compiler.Compiler.generate_five_random_chars')
    @patch('seamlessclient.compiler.get_by_uniquename')
    def test_compile_file_on_filesystem(self, get_by_uniquename_mock, random_mock):
        if MainLoopTests.ignore_this_testcase:
            return
        get_by_uniquename_mock.side_effect = [server_answer_circle, server_answer_arduino]
        random_mock.return_value = "abcde"
        path = os.path.join(test_path, "file.scad")
        event = [path, False]
        file = open(path, "w")
        file.write(test_input)
        file.flush()
        file.close()       
        mainloop.instance.compile_file(*event)
        
        get_by_uniquename_mock.side_effect = [server_answer_circle, server_answer_arduino]
        random_mock.return_value = "abcde"
        output_compare = Compiler().compile(test_input)
        outfile = open(get_filename_for_compiled_file(path), "r")
        output_fromfile = outfile.read()
        outfile.close()
        
        self.assertEqual(output_compare, output_fromfile)
        self.assertTrue(os.path.isfile(get_filename_for_compiled_file(path)))
    
    @patch('seamlessclient.mainloop.instance.should_compile')
    @patch('seamlessclient.mainloop.instance.start_compiler_runner')
    @patch('seamlessclient.mainloop.Watcher')
    def test_start_watch_starts_watch_and_fills_queue(self, watcher, start_compiler_runner, should_compile):
        should_compile.return_value = True
        mainloop.instance.start_watch('/abcdefghi/jklmno')

        self.assertTrue(watcher().start.called)
        self.assertTrue(watcher().set_handler.called)
        self.assertTrue(mainloop.instance.w.start.called)  # @UndefinedVariable
        
        handler = watcher().set_handler.call_args[0][0]
        self.assertEqual(handler, mainloop.file_changed_handler)
        handler("/not/existant/directory", True)
        
        queueitem = mainloop.instance.queue.get()
        self.assertEqual(queueitem[0], "/not/existant/directory")
        self.assertEqual(queueitem[1], True)
        
        self.assertTrue(start_compiler_runner.called)
        
    @patch('seamlessclient.mainloop.instance.start_compiler_runner')
    @patch('seamlessclient.mainloop.Watcher')
    @patch('seamlessclient.mainloop.instance.w')
    def test_start_watch_kills_watch_if_existent(self, w, Watcher, compiler_runner):
        mainloop.instance.start_watch('/abcdefghi/jklmno')

        self.assertTrue(w.stop.called)
        
        
    def test_start_compiler_runner_only_starts_thread_if_no_older_thread_is_running(self):
        mainloop.instance.compiler_thread_is_running = True
        mainloop.instance.start_compiler_runner()
        self.assertTrue(mainloop.instance.compiler_thread is None)
        
    @patch('seamlessclient.mainloop.instance.compile_file')
    def test_new_thread_calls_compiler_for_each_queue_item(self, compile_file):
        this_thread = threading.current_thread()
        other_thread = []
        def catch_thread(a, b):
            other_thread.append(threading.current_thread())
        compile_file.side_effect = catch_thread
        mainloop.instance.queue.put(['/folder2/file2', False])
        mainloop.instance.queue.put(['/folder1/file1', True])
        mainloop.instance.start_compiler_runner()
        mainloop.instance.queue.join()
        mainloop.instance.compiler_thread_request_stop = True
        while mainloop.instance.compiler_thread_is_running:
            time.sleep(0.01)
        time.sleep(0.01)
        self.assertEqual(compile_file.call_args[0][0], '/folder1/file1')
        self.assertNotEqual(other_thread[0], this_thread)
        self.assertEqual(len(other_thread), 2)

    
    @patch('seamlessclient.mainloop.instance.w')
    @patch('seamlessclient.mainloop.instance.compiler_thread')
    def test_stop_mainloop_stops_both_threads(self, compiler_thread, w):
        mainloop.instance.compiler_thread_is_running = True
        mainloop.instance.stop_watch()
        self.assertTrue(w.stop.called)
        self.assertTrue(compiler_thread.join.called)
        
        
    @patch('seamlessclient.mainloop.instance.start_compiler_runner')
    @patch('seamlessclient.mainloop.instance.should_compile')
    def test_files_go_through_decider(self, should_compile, start_compiler_runner):
        should_compile.return_value = False
        mainloop.file_changed_handler("file.scad", True)
        should_compile.assert_called_once_with("file.scad", True)
        self.assertTrue(mainloop.instance.queue.empty())

        should_compile.return_value = True
        mainloop.file_changed_handler("file.scad", True)
        self.assertFalse(mainloop.instance.queue.empty())

    
    def test_can_get_checksum(self):
        file_path = os.path.join(test_path, "test.abc")
        file = open(file_path, "w")
        file.write("123")
        file.close()
        
        sha1 = mainloop.instance.get_checksum(file_path)
        self.assertEqual("40bd001563085fc35165329ea1ff5c5ecbdbbeef", sha1)
        # echo -n 123 | sha1sum
    
    @patch('seamlessclient.mainloop.instance.get_checksum')
    def test_decide_compilation(self, get_checksum):
        # Never seen, never compiled
        get_checksum.side_effect = ['v1', 'v1']
        self.assertTrue(mainloop.instance.should_compile('file.scad', False))
        # same Checksum (File not changed) 
        self.assertFalse(mainloop.instance.should_compile('file.scad', False))
    
    
    