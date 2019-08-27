from src.sender import Sender


class SenderFactory:
    def spawn(self) -> Sender:
        raise NotImplementedError
