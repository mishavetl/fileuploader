class Sender:
    def send(self, filename: str) -> bool:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
