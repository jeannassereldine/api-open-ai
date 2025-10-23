import asyncio
from datetime import time
import json
from graph.graph_excecutor import compile_graph
from models.chat_models import ChatCompletionRequest
from models.documents_models import DocumentsModel
from services.stream_service import process_part, stream_queue
from typing import AsyncGenerator

graph = compile_graph()


import asyncio
import json
from typing import AsyncGenerator

import asyncio
import json
from typing import AsyncGenerator

async def _resp_async_generator(request) -> AsyncGenerator[str, None]:
    state = {"request": request, "is_valid": False}
    invoked_task = asyncio.create_task(graph.ainvoke(state))
    
    
    while True:
        print('ok')
        chunk = await stream_queue.get()
        if chunk == "[DONE]":
            break

        # Start graph.ainvoke exactly once
        if invoked_task is None:
            invoked_task = asyncio.create_task(graph.ainvoke(state))

        yield f"data: {json.dumps(chunk)}\n\n"
    await invoked_task()
    yield "data: [DONE]\n\n"
    process_part("[DONE]")
    # Ensure graph.ainvoke runs at least once and completes5ala
    





async def process_chat_request(request: ChatCompletionRequest):
    if request.messages:
        resp_content = "As a mock AI Assistant, I can only echo your last message:"
    else:
        resp_content = "As a mock AI Assistant, I can only echo your last message, but there wasn't one!"

    return resp_content
