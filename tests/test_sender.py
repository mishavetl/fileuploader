import unittest

from src.sender import Sender


class NotImplementedTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sender = Sender()

    def test_send_method(self):
        self.assertRaises(NotImplementedError, self.sender.send, 'foo.txt')

    def test_close_method(self):
        self.assertRaises(NotImplementedError, self.sender.close)


if __name__ == '__main__':
    unittest.main()
