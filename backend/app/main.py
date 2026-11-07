import time
import logging
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api.routes import api_router

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("agrivision")


# Rate Limiting Middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.clients = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - 60.0

        # Filter out timestamps older than 60s
        self.clients[client_ip] = [ts for ts in self.clients[client_ip] if ts > window_start]

        if len(self.clients[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for client: {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many requests. Please slow down."}
            )

        self.clients[client_ip].append(now)
        return await call_next(request)


# Request Logging Middleware
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"

        response = await call_next(request)

        process_time = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} ({process_time}ms) from {client_host}"
        )
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("Initializing Agrivision AI+ backend services...")
    # Ensure local upload directories exist
    upload_path = Path(settings.STORAGE_LOCAL_DIR).resolve()
    upload_path.mkdir(parents=True, exist_ok=True)
    (upload_path / "diagnoses").mkdir(parents=True, exist_ok=True)
    (upload_path / "explainability").mkdir(parents=True, exist_ok=True)
    (upload_path / "severity").mkdir(parents=True, exist_ok=True)
    (upload_path / "reports").mkdir(parents=True, exist_ok=True)
    (upload_path / "audio").mkdir(parents=True, exist_ok=True)

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {e}")

    yield

    logger.info("Shutting down Agrivision AI+ backend.")


# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade AI-powered agricultural diagnosis, advisory, yield prediction, and multilingual support backend.",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)
app.add_middleware(RequestLoggingMiddleware)

# Mount local uploads for static file access
upload_dir = Path(settings.STORAGE_LOCAL_DIR).resolve()
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root route
@app.get("/", tags=["Root"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.BACKEND_ENV,
        "documentation": f"{settings.API_V1_STR}/docs",
        "status": "operational"
    }


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception at {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "detail": "An internal server error occurred. Our team has been notified."},
    )
