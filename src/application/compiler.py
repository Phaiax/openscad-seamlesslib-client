from application.cachedfetch import get_by_uniquename
from application.webfetch import NotFound
import re

class Compiler(object):
    def __init__(self):
        self.seamless_call_regex = re.compile(r"(?P<uniquename>~[a-zA-Z0-9\-]*)\s*\(")
    
    def compile(self, input):
        self.input = input
        self.find_seamless_calls()
        self.fetch_methods()
        return self.input
    
    def fetch_methods(self):
        self.errors = []
        self.modules = {}
        for uniquename in self.functions:
            try:
                self.modules[uniquename] = get_by_uniquename(uniquename)
            except NotFound as e:
                self.errors.append("Module %s could not be found." % uniquename)
    
    def find_seamless_calls(self):
        scanner = self.seamless_call_regex.scanner(self.input)
        match = scanner.search()
        self.matches = []
        self.functions = []
        while match is not None:
            self.matches.append(match)
            self.functions.append(match.group('uniquename'))
            match = scanner.search()
        self.functions = list(set(self.functions))
        return self.matches, self.functions
