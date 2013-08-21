from application.cachedfetch import get_by_uniquename
from application.webfetch import NotFound
import re
import uuid

class Compiler(object):
    def __init__(self):
        self.seamless_call_regex = re.compile(r"(?P<uniquename>~[a-zA-Z0-9\-]*)\s*\(")
    
    def compile(self, input):
        self.input = input
        self.fetch_and_prepare()
        
        return self.replace_calls_with_randomized_names(self.input) \
            + self.generate_complete_sourcecode_appendix()

    def fetch_and_prepare(self):
        self.find_calls_to_methods_on_seamless_server()
        self.fetch_methods()
        self.generate_all_randomized_module_names()
    
    def fetch_methods(self):
        self.errors = []
        self.modules = {}
        for uniquename in self.calls_to_seamless_modules:
            try:
                self.modules[uniquename] = get_by_uniquename(uniquename) 
            except NotFound as e:
                self.errors.append("Module %s could not be found." % uniquename)
    
    def generate_all_randomized_module_names(self):
        for module in self.modules.values():
            module['randomized_method_name'] = self.randomize_module_name(module['uniquename'][1:])
    
    
    def find_calls_to_methods_on_seamless_server(self):
        scanner = self.seamless_call_regex.scanner(self.input)
        match = scanner.search()
        self.matches = []
        self.calls_to_seamless_modules = []
        while match is not None:
            self.matches.append(match)
            self.calls_to_seamless_modules.append(match.group('uniquename'))
            match = scanner.search()
        self.calls_to_seamless_modules = list(set(self.calls_to_seamless_modules))
        return self.matches, self.calls_to_seamless_modules

    def replace_modulename(self, newname, oldname, sourcecode):
        newname = "module " + newname + "("
        oldname_escaped = re.escape(oldname) 
        regex = re.compile(r"module\s*" + oldname_escaped + r"\s*\(")
        return newname.join(regex.split(sourcecode))
        return sourcecode.replace(oldname, newname)
    
    def generate_five_random_chars(self):
        return uuid.uuid4().__str__()[0:5]    
    
    def randomize_module_name(self, module_name):
        return "%s-%s" % (module_name, self.generate_five_random_chars())

    def generate_complete_sourcecode_appendix(self):
        sourcecodes = [self.replace_modulename(mod['randomized_method_name'], mod['modulename'], 
                mod['sourcecode']) for mod in self.modules.values()]
        return "\n".join(sourcecodes)

    def replace_calls_with_randomized_names(self, input):
        for module in self.modules.values():
            input = input.replace(module['uniquename'], module['randomized_method_name'])
        return input
    