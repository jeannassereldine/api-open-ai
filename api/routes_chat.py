from fastapi import APIRouter
from starlette.responses import StreamingResponse
from models.chat_models import ChatCompletionRequest, Message
from services.chat_service import _resp_async_generator, process_chat_request
import time

router = APIRouter()


@router.post("/completions")
async def chat_completions(request: ChatCompletionRequest):
    # print(request)

    if request.stream:
        return StreamingResponse(
            _resp_async_generator(request), media_type="application/x-ndjson"
        )

    resp_content = await process_chat_request(request)
    return {
        "id": "1337",
        "object": "chat.completion",
        "created": time.time(),
        "model": request.model,
        "choices": [
            {"index": 0, "message": Message(role="assistant", content=resp_content)}
        ],
    }
