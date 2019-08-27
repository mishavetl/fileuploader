from multiprocessing import Queue, Manager, Pool
from multiprocessing.managers import ValueProxy
from typing import List

from src.sender_factory import SenderFactory
from src.worker import Worker


class WorkerManager:
    """Manages worker processes"""

    def __init__(self, sender_factory: SenderFactory, processes: int, queue: Queue, active: ValueProxy):
        self.sender_factory = sender_factory
        self.processes = processes
        self.queue = queue
        self.active = active

    def distribute(self, files: List[str]) -> None:
        with Manager() as manager:
            worker = Worker(self.sender_factory, len(files), self.queue, manager.Value('i', 0), manager.Value('i', 0))
            with Pool(self.processes) as pool:
                pool.map(worker.upload, files)
            self.active.value = False
            worker.notify('')
