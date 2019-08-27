import multiprocessing as mp


def Queue() -> mp.Queue:
    return mp.Manager().Queue()
