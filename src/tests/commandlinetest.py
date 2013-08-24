from application.commandline import run
import application
from mock import patch
import unittest

prints = []

def sys_stdout(string):
    prints.append(string)

class CommandlineTests(unittest.TestCase):
    
    
    def set_up(self):
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
        run(['--help'])
        self.assertTrue('usage' in prints[0])
        
    @patch('application.mainloop.instance.start_watch')
    def test_starts_programm(self, start_watch):
        run(['./watchpath/'])
        start_watch.assert_called_once_with('./watchpath/')
        
        