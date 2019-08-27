from multiprocessing import Queue, Process, Manager
from typing import List

from src.sender_factory import SenderFactory
from src.mock_sender_factory import MockSenderFactory
from src.worker_manager import WorkerManager


class Uploader:
    """Uploads files to a remote server"""

    def __init__(self, files: List[str],
                 processes: int,
                 queue: Queue,
                 sender_factory: SenderFactory = MockSenderFactory()):
        super().__init__()
        self.sender_factory = sender_factory
        self.files = files
        self.files_processed = 0
        self.manager = Manager()
        self.active = self.manager.Value('b', False)
        self.worker_manager = WorkerManager(sender_factory, processes, queue, self.active)

    def start(self) -> Process:
        self.active.value = True
        process = Process(name='manager', target=self.worker_manager.distribute, args=(self.files,))
        process.start()
        return process

    def is_active(self) -> bool:
        return self.active.value
