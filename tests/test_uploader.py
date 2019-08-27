import unittest
from multiprocessing import Manager

from src.uploader import Uploader


class FunctionalityTestCase(unittest.TestCase):
    files = ['foo.txt', 'bar.txt', 'baz.txt', 'quuux.txt', 'quuz.txt']

    def setUp(self) -> None:
        self.manager = Manager()
        self.queue = self.manager.Queue()
        self.uploader = Uploader(self.files, 6, self.queue)

    def test_start_method(self):
        self.assertEqual(self.uploader.is_active(), False)
        process = self.uploader.start()
        for i in range(6):
            self.assertEqual(self.uploader.is_active(), True)
            progress = self.queue.get()
            self.assertNotEqual(progress.done + progress.error, 0)

        process.join()
        self.assertEqual(self.uploader.is_active(), False)


if __name__ == '__main__':
    unittest.main()
