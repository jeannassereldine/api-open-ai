from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes_chat import router as chat_router
from api.routes_document import router as document_router
from core.exceptions import validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    yield
    
app = FastAPI(title="lc api",lifespan=lifespan )  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],     # allow POST, OPTIONS, GET, etc.
    allow_headers=["*"],
)
  
app.mount("/output", StaticFiles(directory="output"), name="output")
# Register routes
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(document_router,prefix="/documents")


# Register exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
