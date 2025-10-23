from fastapi import FastAPI
from api.routes_chat import router as chat_router
from core.exceptions import validation_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="OpenAI-compatible API")

# Register routes
app.include_router(chat_router, prefix="/chat", tags=["chat"])

# Register exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
