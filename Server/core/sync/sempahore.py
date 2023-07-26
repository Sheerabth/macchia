from threading import Lock, Semaphore


class CustomSemaphore:
    def __init__(self, value: int) -> None:
        self.semaphore = Semaphore(value)
        self.waiting = 0
        self.count_lock = Lock()

    def acquire(self):
        self.count_lock.acquire()
        self.waiting += 1
        self.count_lock.release()
        self.semaphore.acquire()

    def release(self):
        self.semaphore.release()
        self.count_lock.acquire()
        self.waiting -= 1
        self.count_lock.release()

    def release_all(self):
        print(f"Releasing {self.waiting} threads")
        if self.waiting != 0:
            self.semaphore.release(self.waiting)
        self.count_lock.acquire()
        self.waiting = 0
        self.count_lock.release()