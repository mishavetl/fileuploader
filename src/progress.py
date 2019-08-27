class Progress:
    """Stores progress information"""

    def __init__(self, file: str, done: int, error: int, total: int):
        self.file = file
        self.done = done
        self.error = error
        self.total = total
