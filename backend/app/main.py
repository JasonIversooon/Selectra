from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as api_router
from .core.config import BACKEND_ALLOWED_ORIGINS, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SEC
from collections import deque
import time
import time, logging, hashlib

logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    app = FastAPI(title="Selectra Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if BACKEND_ALLOWED_ORIGINS == "*" else BACKEND_ALLOWED_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Simple in-memory rate limiter (NOT for production scale)
    _rl_store = {}

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        action = None
        cache_hit = request.headers.get("x-cache-hit")
        # Rate limiting
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = RATE_LIMIT_WINDOW_SEC
        limit = RATE_LIMIT_REQUESTS
        dq = _rl_store.get(ip)
        if dq is None:
            dq = deque()
            _rl_store[ip] = dq
        # Drop old
        while dq and dq[0] <= now - window:
            dq.popleft()
        if len(dq) >= limit:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=429, content={"detail": "rate limit exceeded"})
        dq.append(now)
        try:
            response = await call_next(request)
            # Expose simplistic rate limit remaining header
            if ip in _rl_store:
                remaining = max(0, RATE_LIMIT_REQUESTS - len(_rl_store[ip]))
                response.headers["X-RateLimit-Remaining"] = str(remaining)
            status = response.status_code
            duration_ms = int((time.time() - start) * 1000)
            logger.info("req path=%s status=%s dur_ms=%s", request.url.path, status, duration_ms)
            return response
        except Exception:
            duration_ms = int((time.time() - start) * 1000)
            logger.exception("Unhandled error path=%s dur_ms=%s", request.url.path, duration_ms)
            raise

    app.include_router(api_router)
    return app


app = create_app()
