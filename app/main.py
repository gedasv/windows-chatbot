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

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Custom logging middleware for FastAPI.
    I would put this in a separate file, but it's a small project.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log information about it.
        Logs the request method, path, status code, and processing time for each request.
        
        :param request: The incoming request object
        :param call_next: The next middleware or route handler in the chain
        :return: The response from the next middleware or route handler
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
        return response

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    
    :param app: The FastAPI application instance
    """
    logger.info("Application is starting up")
    yield
    logger.info("Application is shutting down")

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application. Initialize middleware.
    
    :return: The configured FastAPI application instance
    """
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
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

def setup_routes(app: FastAPI) -> None:
    """
    Set up the routes for the application.

    :param app: The FastAPI application instance
    """
    app.include_router(
        chat_routes.router,
        prefix="/api",
        dependencies=[Depends(get_chat_service)]
    )

    @app.get("/")
    async def root() -> dict:
        """
        Root endpoint.
        
        :return: A welcome message dictionary
        """
        return {"message": "Welcome to the Window Manufacturing Chatbot API"}

    @app.get("/health")
    async def health_check() -> dict:
        """
        Health check endpoint.
        
        :return: A dictionary indicating the health status of the application
        """
        return {"status": "healthy"}

def get_llm_service():
    """
    Dependency injection function for LLMService.
    
    :return: An instance of LLMService
    """
    return LLMService()

def get_context_manager():
    """
    Dependency injection function for ContextManager.
    
    :return: An instance of ContextManager
    """
    return ContextManager()

def get_chat_service(
    llm_service: LLMService = Depends(get_llm_service),
    context_manager: ContextManager = Depends(get_context_manager)
) -> ChatService:
    """
    Dependency injection function for ChatService.
    
    :param llm_service: An instance of LLMService
    :param context_manager: An instance of ContextManager
    :return: An instance of ChatService
    """
    return ChatService(llm_service, context_manager)

app = create_application()
setup_routes(app)