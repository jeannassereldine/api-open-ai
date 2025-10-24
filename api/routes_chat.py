from fastapi import APIRouter
from starlette.responses import StreamingResponse
from models.chat_models import AnalyseLCRequest
from services.chat_service import _resp_async_generator
import time

router = APIRouter()



@router.post("/analyse_lc_documents")
async def chat_completions(request: AnalyseLCRequest):
    # print(request)
 return StreamingResponse(_resp_async_generator(request), media_type="application/x-ndjson")

  
