import asyncio
from datetime import time
import json
from graph.graph_excecutor import compile_graph
from models.chat_models import ChatCompletionRequest
from models.documents_models import DocumentsModel
from typing import AsyncGenerator
graph = compile_graph()
import asyncio
import json
from typing import AsyncGenerator

import asyncio
import json
from typing import AsyncGenerator
from datetime import datetime


async def _resp_async_generator(request) -> AsyncGenerator[str, None]:
    state = {"request": request, "is_valid": False}
    index = 0
    for chunk in graph.stream(input=state, stream_mode="custom"):
        print("Yielding chunk:", chunk)
        id_counter ="toto"
        
        chunk = {
        "id": str(id_counter),
        "object": "chat.completion.chunk",
        "created":datetime.now().timestamp(),
        "model": "qwen3-vl:235b-cloud",
        "choices": [{"index": index, "delta": {"content": chunk}}],
       }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0)  # Simulate processing delay
        
        index += 1
        
        # yield f"data: {chunk}\n\n"
        
    
    yield "data: [DONE]\n\n"
    
    
    
    

async def process_chat_request(request: ChatCompletionRequest):
    if request.messages:
        resp_content = "As a mock AI Assistant, I can only echo your last message:"
    else:
        resp_content = "As a mock AI Assistant, I can only echo your last message, but there wasn't one!"

    return resp_content
