import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LogWatcher(FileSystemEventHandler):
    def __init__(self, callback, target_filename):
        self.callback = callback
        self.target_filename = target_filename

    def on_modified(self, event):
        # Dispara o callback apenas se o arquivo modificado for o nosso log alvo
        if not event.is_directory and event.src_path.endswith(self.target_filename):
            self.callback(event.src_path)


def start_watching(path_to_watch, callback):
    target_dir = os.path.dirname(os.path.abspath(path_to_watch))
    target_file = os.path.basename(path_to_watch)

    event_handler = LogWatcher(callback, target_file)
    observer = Observer()

    # Monitora apenas o diretório onde o arquivo está
    observer.schedule(event_handler, target_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Mantém o script rodando em loop infinito
    except KeyboardInterrupt:
        observer.stop()
        print("\n[!] Encerrando vigilância do Agente.")

    observer.join()