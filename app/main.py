# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
import logging
from typing import Any

from .routers import auth, categories, income, spending, savings, users
from .database import engine
from . import models
from .exceptions import AppException

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="FinTrack API",
    description="Financial Tracker API for managing income, expenses, and savings",
    version="1.0.0"
)
# Include Routers
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(income.router)
app.include_router(spending.router)
app.include_router(savings.router)
app.include_router(users.router)

# Health Check Endpoint
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "FinTrack API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Error response helper
def error_response(message: str, status_code: int, details: Any = None):
    return {
        "success": False,
        "error": {
            "message": message,
            "status_code": status_code,
            "details": details
        }
    }

# Success response helper
def success_response(data: Any, message: str = None):
    response = {
        "success": True,
        "data": data
    }
    if message:
        response["message"] = message
    return response

# Exception Handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException: {exc.message} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.message, exc.status_code)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()} - Path: {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="Validation error",
            status_code=422,
            details=exc.errors()
        )
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)} - Path: {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            message="An unexpected error occurred. Please try again later.",
            status_code=500
        )
    )

