import random
import time

from src.sender import Sender


class MockSender(Sender):
    def send(self, filename: str) -> bool:
        time.sleep(random.randint(2, 10) / 10)
        return random.randint(1, 5) != 1

    def close(self) -> None:
        self.send('close.txt')
