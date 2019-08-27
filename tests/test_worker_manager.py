import unittest
from multiprocessing import Manager, Process

from src.mock_sender_factory import MockSenderFactory
from src.worker_manager import WorkerManager


class FunctionalityTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = Manager()
        self.queue = self.manager.Queue()
        self.active = self.manager.Value('b', False)
        self.worker_manager = WorkerManager(MockSenderFactory(), 6, self.queue, self.active)

    def test_distribute_empty(self):
        self.active.value = True
        process = Process(target=self.worker_manager.distribute,
                          args=([],))
        process.start()
        process.join()
        self.assertEqual(self.active.value, False)

    def test_distribute_normal(self):
        self.active.value = True
        process = Process(target=self.worker_manager.distribute,
                          args=(['foo.txt', 'bar.txt', 'baz.txt', 'quuux.txt', 'quuz.txt'],))
        process.start()
        for i in range(6):
            progress = self.queue.get()
            self.assertNotEqual(progress.done + progress.error, 0)
        process.join()
        self.assertEqual(self.active.value, False)


if __name__ == '__main__':
    unittest.main()
