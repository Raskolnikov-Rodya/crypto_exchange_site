import time
from collections import defaultdict, deque
from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class LimitWindow:
    max_requests: int
    window_seconds: int


class AuthRateLimiter:
    """Simple in-memory limiter for auth-sensitive routes.

    Keyed by (client_ip, route_key). Suitable for single-instance MVP.
    """

    def __init__(self, login_window: LimitWindow, register_window: LimitWindow):
        self.login_window = login_window
        self.register_window = register_window
        self._events: dict[tuple[str, str], deque[float]] = defaultdict(deque)

    def _active_window(self, route_key: str) -> LimitWindow:
        if route_key == "login":
            return self.login_window
        if route_key == "register":
            return self.register_window
        return LimitWindow(max_requests=10_000, window_seconds=60)

    def check(self, client_ip: str, route_key: str) -> None:
        cfg = self._active_window(route_key)
        key = (client_ip, route_key)
        now = time.time()
        q = self._events[key]

        while q and now - q[0] > cfg.window_seconds:
            q.popleft()

        if len(q) >= cfg.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

        q.append(now)
