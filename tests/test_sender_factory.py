import unittest

from src.sender_factory import SenderFactory


class NotImplementedTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sender_factory = SenderFactory()

    def test_spawn_method(self):
        self.assertRaises(NotImplementedError, self.sender_factory.spawn)


if __name__ == '__main__':
    unittest.main()
