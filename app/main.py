import logging
import time
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.api import chat_routes
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.utils.context_manager import ContextManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom logging middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
        return response

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is starting up")
    yield
    logger.info("Application is shutting down")

def create_application() -> FastAPI:
    app = FastAPI(
        title="Window Manufacturing Chatbot",
        description="API for a chatbot specializing in window manufacturing",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Add middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Update this for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

def setup_routes(app: FastAPI) -> None:
    """
    Set up the routes for the application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(
        chat_routes.router,
        prefix="/api",
        dependencies=[Depends(get_chat_service)]
    )

    @app.get("/")
    async def root() -> dict:
        """Root endpoint."""
        return {"message": "Welcome to the Window Manufacturing Chatbot API"}

    @app.get("/health")
    async def health_check() -> dict:
        """Health check endpoint."""
        return {"status": "healthy"}

# Dependency injection
def get_llm_service():
    return LLMService()

def get_context_manager():
    return ContextManager()

def get_chat_service(
    llm_service: LLMService = Depends(get_llm_service),
    context_manager: ContextManager = Depends(get_context_manager)
) -> ChatService:
    return ChatService(llm_service, context_manager)

app = create_application()
setup_routes(app)