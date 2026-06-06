import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse, PlainTextResponse

from app.api import agents, knowledge, workflows
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.metrics import metrics
from app.db.init_db import init_db

settings = get_settings()
configure_logging(settings.log_level)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", default_response_class=ORJSONResponse, lifespan=lifespan)

@app.middleware("http")
async def correlation_and_metrics(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = str(round((time.perf_counter() - start) * 1000, 2))
    metrics.inc(f"http_{request.method.lower()}_{response.status_code}")
    return response


@app.get("/", tags=["System"])
async def root() -> dict:
    return {
        "service": settings.app_name,
        "status": "running",
        "environment": settings.environment,
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
        "api_base": "/api/v1",
    }

@app.get("/health", tags=["System"])
async def health() -> dict:
    return {"status": "ok", "service": settings.app_name, "environment": settings.environment}

@app.get("/metrics", response_class=PlainTextResponse, tags=["System"])
async def prometheus_metrics() -> str:
    return metrics.render_prometheus()

app.include_router(agents.router, prefix="/api/v1")
app.include_router(knowledge.router, prefix="/api/v1")
app.include_router(workflows.router, prefix="/api/v1")
