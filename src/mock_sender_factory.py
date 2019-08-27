from src.sender_factory import SenderFactory
from src.mock_sender import MockSender


class MockSenderFactory(SenderFactory):
    def spawn(self) -> MockSender:
        return MockSender()
