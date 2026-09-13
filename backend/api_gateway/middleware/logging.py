import time
from starlette.middleware.base import BaseHTTPMiddleware
from ml.utils.logger import logging


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logging.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - Duration: {process_time:.2f}ms"
        )
        return response
