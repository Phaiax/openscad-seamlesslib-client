from mock import patch
from seamlessclient.commandline import run
from seamlessclient.version import not_up_to_date_message
import seamlessclient
import unittest

prints = []

def sys_stdout(string):
    prints.append(string)

class CommandlineTests(unittest.TestCase):
    
    
    def setUp(self):
        try:
            while True:
                prints.pop()
        except:
            pass
    
    @patch('argparse._sys.stderr')
    @patch('argparse._sys.stdout')
    @patch('argparse._sys.exit')
    def test_print_help(self, _exit, stdout_mock, stderr_mock):
        stdout_mock.write.side_effect = sys_stdout
        stderr_mock.write.side_effect = sys_stdout
        self.assertEqual(0, len(prints))
        run(['--help'])
        self.assertIn('usage', prints[0])
        
    @patch('seamlessclient.mainloop.instance.start_watch')
    def test_starts_programm(self, start_watch):
        run(['./watchpath/'])
        start_watch.assert_called_once_with('./watchpath/')
        
    @patch('seamlessclient.commandline._sys.stderr')
    @patch('seamlessclient.commandline._sys.stdout')
    @patch('seamlessclient.commandline._sys.exit')
    @patch('seamlessclient.version.is_this_client_supported')
    def test_displays_nice_unsupported_version_message(self, 
                                                       is_this_client_supported, 
                                                       _exit, 
                                                       stdout_mock, 
                                                       stderr_mock):
        is_this_client_supported.return_value = False
        stdout_mock.write.side_effect = sys_stdout
        stderr_mock.write.side_effect = sys_stdout
        run(['./watchpath/'])
        self.assertFalse('Traceback' in prints[0])
        self.assertTrue(not_up_to_date_message[0:20] in prints[0])
        self.assertTrue(_exit.called)
        