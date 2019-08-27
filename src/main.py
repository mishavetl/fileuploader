import sys

from . import queue
from .uploader import Uploader


def print_help_message() -> None:
    print(sys.argv[0] + ' [files to upload] [-h]')


class Main:
    """Initializes executable application"""

    def __init__(self, workers: int):
        self.q = queue.Queue()
        self.uploader = Uploader(sys.argv[1:], workers, self.q)

    def upload_files(self) -> None:
        self.uploader.start()
        self.loop()

    def output_progress(self) -> None:
        progress = self.q.get()
        print(progress.file, progress.done, progress.error, progress.total)

    def loop(self) -> None:
        while self.uploader.is_active():
            self.output_progress()

    def run(self) -> None:
        if '-h' in sys.argv:
            print_help_message()
        else:
            self.upload_files()
