# TODO 未实现
#import os
#import time
#import logging
#import threading
#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler
#from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
#if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)
    #event_handler = LoggingEventHandler()
    #observer = Observer()
    #path = ''
    #observer.schedule(event_handler, path, recursive=True)
    #observer.start()
    #try:
        #while True:
            #time.sleep(1)
    #finally:
        #observer.stop()
        #observer.join()
#class FileEventHandler(FileSystemEventHandler):
#    def __init__(self, aim_path):
#        FileSystemEventHandler.__init__(self)
#        self.aim_path = aim_path
#        self.timer = None
#        self.snapshot = DirectorySnapshot(self.aim_path)
#        
#    def on_any_event(self, event):
#        if self.timer:
#            self.timer.cancel()
#        
#        self.timer = threading.Timer(5.5, self.checkSnapshot)
#        self.timer.start()
#    
#    def checkSnapshot(self):
#        snapshot = DirectorySnapshot(self.aim_path)
#        diff = DirectorySnapshotDiff(self.snapshot, snapshot)
#        self.snapshot = snapshot
#        self.timer = None
#        
#        print("files_created:", diff.files_created)
#        print("files_deleted:", diff.files_deleted)
#       print("files_modified:", diff.files_modified)
#        print("files_moved:", diff.files_moved)
#        print("dirs_modified:", diff.dirs_modified)
#        print("dirs_moved:", diff.dirs_moved)
#        print("dirs_deleted:", diff.dirs_deleted)
#        print("dirs_created:", diff.dirs_created)
#   
#class DirMonitor(object):
#    
#    def __init__(self, aim_path):
#        
#        self.aim_path= aim_path
#        self.observer = Observer()
#    
#    def start(self):
#        
#        event_handler = FileEventHandler(self.aim_path)
#        self.observer.schedule(event_handler, self.aim_path, True)
#        self.observer.start()
#    
#    def stop(self):
#        
#        self.observer.stop()
#    
#if __name__ == "__main__":
#    monitor = DirMonitor(r"")
#    monitor.start()
#    try:
#        while True:
#            time.sleep(1)
#    finally:
#        monitor.stop()
#        monitor.observer.join()