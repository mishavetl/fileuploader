from multiprocessing import Queue
from multiprocessing.managers import ValueProxy

from src.progress import Progress
from src.sender_factory import SenderFactory


class Worker:
    """Manages progress uploading"""

    def __init__(self,
                 sender_factory: SenderFactory,
                 files_count: int,
                 queue: Queue,
                 done: ValueProxy,
                 failed: ValueProxy):
        self.sender_factory = sender_factory
        self.files_count = files_count
        self.queue = queue
        self.done = done
        self.failed = failed

    def handle_result(self, result: bool) -> None:
        if result:
            self.done.value += 1
        else:
            self.failed.value += 1

    def upload(self, file: str) -> None:
        sender = self.sender_factory.spawn()
        result = sender.send(file)
        sender.close()
        self.handle_result(result)
        self.notify(file)

    def notify(self, file) -> None:
        self.queue.put(Progress(file, self.done.value, self.failed.value, self.files_count))
