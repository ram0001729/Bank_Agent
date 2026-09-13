import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

# Prometheus Metrics Definitions
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total count of HTTP requests",
    ["method", "endpoint", "status"]
)

AGENT_EXECUTIONS_TOTAL = Counter(
    "agent_executions_total",
    "Total agent workflow executions",
    ["agent_name", "action", "status"]
)

GOVERNANCE_DENIALS_TOTAL = Counter(
    "governance_denials_total",
    "Total actions denied by Governance OS",
    ["agent_name", "reason"]
)

FRAUD_DETECTIONS_TOTAL = Counter(
    "fraud_detections_total",
    "Total fraud attempts detected by XGBoost model",
    ["risk_level"]
)

REQUEST_LATENCY_SECONDS = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        endpoint = request.url.path
        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(response.status_code)
        ).inc()

        REQUEST_LATENCY_SECONDS.labels(endpoint=endpoint).observe(duration)
        return response


def get_prometheus_metrics():
    return generate_latest(), CONTENT_TYPE_LATEST
