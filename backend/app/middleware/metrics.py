"""
Prometheus metrics middleware for monitoring
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
active_requests = Gauge('http_requests_active', 'Active HTTP requests')
llm_requests = Counter('llm_requests_total', 'Total LLM requests', ['model', 'task_type'])
llm_tokens = Counter('llm_tokens_total', 'Total tokens used', ['model'])
llm_errors = Counter('llm_errors_total', 'LLM errors', ['model', 'error_type'])
cache_hits = Counter('cache_hits_total', 'Cache hits')
cache_misses = Counter('cache_misses_total', 'Cache misses')


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip metrics endpoint
        if request.url.path == "/metrics":
            return await call_next(request)
        
        active_requests.inc()
        start_time = time.time()
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            request_count.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            request_duration.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            return response
        finally:
            active_requests.dec()


async def metrics_endpoint(request: Request):
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
