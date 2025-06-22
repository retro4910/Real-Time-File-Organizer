import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Folder to watch (you can change this to your Downloads folder)
WATCHED_FOLDER = os.path.expanduser("~/Downloads")

#  Folder categories

file_types = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Videos': ['..mp4', '.mkv', '.avi', '.mov'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'codes': ['.py', '.js', '.html', '.css', '.cpp', '.java']
}

class FileMoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1) # Wait for file to be fully written
            self.organize_file(event.src_path)

    def organize_file(self, path):
        filename = os.path.basename(path)
        ext = os.path.splitext(filename)[1].lower()
        move = False
        for folder, extensions in file_types.items.items():
            if ext in extensions:
                target_folder = os.path.join(WATCHED_FOLDER, folder)
                os.makedir(target_folder, exist_ok = True)
                shutil.move(path, os.path.join(target_folder, filename))
                moved = True
                print(f"Moved {filename} to Others/")

if __name__ == "__main__":
    print(f"Watching folder: {WATCHED_FOLDER}")
    event_handler = FileMoverHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive = False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()