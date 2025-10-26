from fastapi import APIRouter
from starlette.responses import StreamingResponse
from models.chat_models import AnalyseLCRequest, ResumeRequest
from services.chat_service import _resp_async_generator

router = APIRouter()
@router.post("/analyse_lc_documents")
async def chat_completions(req: AnalyseLCRequest):
 return StreamingResponse(_resp_async_generator(req), media_type="application/x-ndjson")

  
@router.post("/resume_analysing_lc_document")
async def resume_workflow(req: ResumeRequest):
   return StreamingResponse(_resp_async_generator(req), media_type="application/x-ndjson")
