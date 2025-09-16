import time
from collections import deque

class RateLimiter:
    def __init__(self, max_per_minute: int = 40):
        self.max = max_per_minute
        self.q = deque()

    def acquire(self):
        now = time.time()
        window_start = now - 60
        while self.q and self.q[0] < window_start:
            self.q.popleft()
        if len(self.q) >= self.max:
            sleep_for = 60 - (now - self.q[0])
            if sleep_for > 0:
                time.sleep(sleep_for)
        self.q.append(time.time())
