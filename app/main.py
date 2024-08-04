from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging
import time
from typing import Callable

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
    # Startup logic
    logger.info("Application is starting up")
    # You could initialize resources here, e.g., database connections
    yield
    # Shutdown logic
    logger.info("Application is shutting down")
    # You could clean up resources here, e.g., close database connections

# Create FastAPI app
app = FastAPI(title="Window Manufacturing Chatbot", lifespan=lifespan)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
def get_llm_service():
    return LLMService()

def get_context_manager():
    return ContextManager()

def get_chat_service(
    llm_service: LLMService = Depends(get_llm_service),
    context_manager: ContextManager = Depends(get_context_manager)
):
    return ChatService(llm_service, context_manager)


# Include routers
app.include_router(
    chat_routes.router,
    prefix="/api",
    dependencies=[Depends(get_chat_service)]
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Window Manufacturing Chatbot API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}