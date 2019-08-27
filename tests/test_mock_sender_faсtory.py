import unittest

from src.mock_sender import MockSender
from src.mock_sender_factory import MockSenderFactory


class FunctionalityTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_sender_factory = MockSenderFactory()

    def test_spawn_method(self):
        self.assertIsInstance(self.mock_sender_factory.spawn(), MockSender)


if __name__ == '__main__':
    unittest.main()
