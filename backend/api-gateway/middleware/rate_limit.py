import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        if client_ip not in self.clients:
            self.clients[client_ip] = []

        # Keep requests within time window
        self.clients[client_ip] = [
            t for t in self.clients[client_ip]
            if now - t < self.window_seconds
        ]

        if len(self.clients[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

        self.clients[client_ip].append(now)
        return await call_next(request)
