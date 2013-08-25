from Queue import Empty
from seamlessclient.compiler import Compiler
from seamlessclient.config import Config
from seamlessclient.filenames import get_filename_for_compiled_file
from seamlessclient.filesystemwatcher import Watcher
from seamlessclient.webfetch import make_user_url
import Queue
import hashlib
import os
import threading

instance = None

class MainLoop(object):
    def __init__(self):
        if instance is not None:
            raise Exception()
        self.w = None
        self.queue = Queue.Queue()
        self.compiler_thread_is_running = False
        self.compiler_thread_request_stop = False
        self.compiler_thread = None
        self.compiled_files = {}

    def compile_file(self, scadfile, compiled_file_exists):
        infile = open(scadfile, "r")
        outfile = self.create_file_if_not_exists_and_open(get_filename_for_compiled_file(scadfile))
        input = infile.read()
        c = Compiler()
        output = c.compile(input)
        outfile.write(output)
        infile.close()
        outfile.close()
        for error in c.errors:
            print error
        for module in c.modules.values():
            url = make_user_url(Config().get_server(), module['guid'])
            print "%s: %s (%s) %s" % (module['uniquename'], module['title'], module['description'], url)
        
    def start_compiler_runner(self):
        def compiler_runner():
            self.compiler_thread_is_running = True
            while not self.compiler_thread_request_stop:
                try:
                    scadfile, compiled_file_exists = self.queue.get(timeout=0.2)
                    self.compile_file(scadfile, compiled_file_exists)
                    self.queue.task_done()
                except Empty:
                    pass
            self.compiler_thread_is_running = False
        if not self.compiler_thread_is_running:
            self.compiler_thread = threading.Thread(target=compiler_runner)
            self.compiler_thread_request_stop = False
            self.compiler_thread.daemon = True
            self.compiler_thread.start()
        
        
    def create_file_if_not_exists_and_open(self, filename):
        if not os.path.isfile(filename):
            open(filename, "a").close()
        return open(filename, "w")
    
    def is_running(self):
        return self.w is not None or self.compiler_thread is not None
    
    def start_watch(self, base_path):
        if self.w is not None:
            self.stop_watch()
        self.w = Watcher(base_path)
        self.w.set_handler(file_changed_handler)
        self.w.start()
        self.start_compiler_runner()
        print "Started to watch %s" % base_path
        
    def stop_watch(self):
        if self.w is not None:
            self.w.stop()
            self.w = None
            print "Watcher stopped    ",
        try:
            while True:
                self.queue.get_nowait()
                self.queue.task_done()
        except:
            print "Queue emptied    ",
        if self.compiler_thread is not None:
            self.compiler_thread_request_stop = True
            # self.queue.join()
            print "Queue joined    ",
            self.compiler_thread.join(3)
            print "Compiler Thread joined    ",
            self.compiler_thread = None
        print 
        
    def get_checksum(self, scadfile):
        afile = open(scadfile, "r")
        hasher = hashlib.sha1()
        buf = afile.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(65536)
        return hasher.hexdigest()
    
    def should_compile(self, scadfile, compiled_file_exists):
        checksum = self.get_checksum(scadfile)
        if scadfile in self.compiled_files:
            last_compiled_with_checksum = self.compiled_files[scadfile]
            if checksum != last_compiled_with_checksum:
                self.compiled_files[scadfile] = checksum
                return True
            return False
        else:
            self.compiled_files[scadfile] = checksum
            return True
        

def file_changed_handler(scadfile, compiled_file_exists):
    if instance.should_compile(scadfile, compiled_file_exists):
        print "\n ## Change detected: %s" % scadfile,
        instance.queue.put([scadfile, compiled_file_exists])
        print " -> compile"
    else:
        pass
        # print " | already up to date"

instance = MainLoop()
