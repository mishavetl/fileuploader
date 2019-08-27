import unittest
from multiprocessing import Manager, Process

from src.mock_sender_factory import MockSenderFactory
from src.worker import Worker


class FunctionalityTestCase(unittest.TestCase):
    files = ['foo.txt', 'bar.txt']

    def setUp(self) -> None:
        self.manager = Manager()
        self.queue = self.manager.Queue()
        self.done = self.manager.Value('i', 0)
        self.failed = self.manager.Value('i', 0)
        self.worker = Worker(MockSenderFactory(), len(self.files), self.queue, self.done, self.failed)

    def test_handle_result_done(self):
        process = Process(target=self.worker.handle_result, args=(True,))
        process.start()
        process.join()
        self.assertEqual(self.done.value, 1)
        self.assertEqual(self.failed.value, 0)

    def test_handle_result_failed(self):
        process = Process(target=self.worker.handle_result, args=(False,))
        process.start()
        process.join()
        self.assertEqual(self.done.value, 0)
        self.assertEqual(self.failed.value, 1)

    def test_notify_initial(self):
        process = Process(target=self.worker.notify, args=('foo.txt',))
        process.start()
        progress = self.queue.get()
        self.assertEqual(progress.file, 'foo.txt')
        self.assertEqual(progress.done, 0)
        self.assertEqual(progress.error, 0)
        self.assertEqual(progress.total, 2)
        process.join()

    def test_notify_one_done_one_failed(self):
        handle_result = Process(target=self.worker.handle_result, args=(True,))
        handle_result.start()
        handle_result.join()
        notify = Process(target=self.worker.notify, args=('foo.txt',))
        notify.start()
        progress = self.queue.get()
        self.assertEqual(progress.file, 'foo.txt')
        self.assertEqual(progress.done, 1)
        self.assertEqual(progress.error, 0)
        self.assertEqual(progress.total, 2)
        notify.join()
        handle_result = Process(target=self.worker.handle_result, args=(False,))
        handle_result.start()
        handle_result.join()
        notify = Process(target=self.worker.notify, args=('bar.txt',))
        notify.start()
        progress = self.queue.get()
        self.assertEqual(progress.file, 'bar.txt')
        self.assertEqual(progress.done, 1)
        self.assertEqual(progress.error, 1)
        self.assertEqual(progress.total, 2)
        notify.join()

    def test_notify_two_done(self):
        handle_result = Process(target=self.worker.handle_result, args=(True,))
        handle_result.start()
        handle_result.join()
        notify = Process(target=self.worker.notify, args=('foo.txt',))
        notify.start()
        progress = self.queue.get()
        self.assertEqual(progress.file, 'foo.txt')
        self.assertEqual(progress.done, 1)
        self.assertEqual(progress.error, 0)
        self.assertEqual(progress.total, 2)
        notify.join()
        handle_result = Process(target=self.worker.handle_result, args=(True,))
        handle_result.start()
        handle_result.join()
        notify = Process(target=self.worker.notify, args=('bar.txt',))
        notify.start()
        progress = self.queue.get()
        self.assertEqual(progress.file, 'bar.txt')
        self.assertEqual(progress.done, 2)
        self.assertEqual(progress.error, 0)
        self.assertEqual(progress.total, 2)
        notify.join()

    def test_upload(self):
        process = Process(target=self.worker.upload, args=('foo.txt',))
        process.start()
        progress = self.queue.get()
        self.assertEqual(progress.file, 'foo.txt')
        self.assertEqual(progress.done, self.done.value)
        self.assertEqual(progress.error, self.failed.value)
        self.assertEqual(progress.total, 2)
        process.join()


if __name__ == '__main__':
    unittest.main()
