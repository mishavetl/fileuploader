import time
import unittest

from src.mock_sender import MockSender


class FunctionalityTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_sender = MockSender()

    def test_send_emulates_different_file_sizes(self):
        ts, ts1 = 0, 0
        while abs(ts1 - ts) < 0.2:
            ts = time.time()
            self.mock_sender.send('foo.txt')
            ts = time.time() - ts
            ts1 = time.time()
            self.mock_sender.send('bar.txt')
            ts1 = time.time() - ts1
        self.assertGreater(abs(ts1 - ts), 0.2)

    def infinite_send(self) -> bool:
        result = True
        while result:
            result = self.mock_sender.send('foo')
        return result

    def test_send_fails_at_least_once(self):
        self.assertFalse(self.infinite_send())

    def test_close_emulates_networking(self):
        ts, ts1 = 0, 0
        while abs(ts1 - ts) < 0.2:
            self.mock_sender = MockSender()
            ts = time.time()
            self.mock_sender.close()
            ts = time.time() - ts
            self.mock_sender = MockSender()
            ts1 = time.time()
            self.mock_sender.close()
            ts1 = time.time() - ts1
        self.assertGreater(abs(ts1 - ts), 0.2)


if __name__ == '__main__':
    unittest.main()
