
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main import grabarVideo
import time
from config import directorio_origen_video

directorioAnalizado = directorio_origen_video

class MyHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        time.sleep(20)
        ficheroNuevo = event.src_path.strip()[-21:-4]
        grabarVideo(ficheroNuevo)
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, directorioAnalizado, recursive=False)
observer.start()

while True:
    try:
        pass
    except KeyboardInterrupt:
        observer.stop()