from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from application.filenames import get_filename_for_compiled_file, has_scad_extension, is_compiled_file, NotAScadFile


class Watcher(FileSystemEventHandler):
    def __init__(self, path = '.'):
        self.path = path
        self.changed_files = []
        self.handler = None
        
    def start(self):
        self.observer = Observer()
        self.observer.schedule(self, path=self.path, recursive=True)
        self.observer.start()
        
    def set_handler(self, handler):
        self.handler = handler
        
    def process_event(self, path):
        if not os.path.isdir(path) and has_scad_extension(path) and not is_compiled_file(path):
            compiled_file_exists = os.path.isfile(get_filename_for_compiled_file(path))
            self.changed_files.append([path, compiled_file_exists])
            if self.handler is not None:
                self.handler(path, compiled_file_exists)
        
    def on_created(self, event):
        FileSystemEventHandler.on_created(self, event)
        # Creation also fires modification event
        #self.process_event(event.src_path)
        return True
        
    def on_modified(self, event):
        FileSystemEventHandler.on_modified(self, event)
        self.process_event(event.src_path)
        return True
        
    def on_moved(self, event):
        FileSystemEventHandler.on_moved(self, event)
        self.process_event(event.dest_path)
        return True
        
    def stop(self):
        self.observer.stop()
        self.observer.join()