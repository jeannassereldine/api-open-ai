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


async def create_chunk(index: int, content, chunk_type: str = "stream"):
    """
    Create a JSON-compatible SSE chunk with metadata and content.
    """
    id_counter = "toto"
    chunk = {
        "id": str(id_counter),
        "object": "chat.completion.chunk",
        "created": datetime.now().timestamp(),
        "model": "qwen3-vl:235b-cloud",
        "choices": [
            {"index": index, "delta": {"type": chunk_type, "content": content}}
        ],
    }
    return f"data: {json.dumps(chunk)}\n\n"


async def _resp_async_generator(request) -> AsyncGenerator[str, None]:
    """
    Async generator to stream chunks from LangGraph including interrupts.
    """
    config = {"configurable": {"thread_id": "thread-1"}}
    state = {"request": request, "is_valid": False}
    index = 0

    for event_type, payload in graph.stream(
        input=state, stream_mode=["custom", "updates"], config=config
    ):
        print("Yielding chunk:", (event_type, payload))

        #  Handle INTERRUPT (pause and ask user)
        if event_type == "updates" and "__interrupt__" in payload:
            interrupt_obj = payload["__interrupt__"][0]
            question = interrupt_obj.value.get("question")
            interrupt_id = interrupt_obj.id
            print(f"Interrupt received: {question} (id={interrupt_id})")
            yield await create_chunk(index, question, "stream")
            # interrupt_data = {
            #     "type": "interrupt",
            #     "id": interrupt_id,
            #     "question": question,
            # }
            # yield await create_chunk(index, interrupt_data, "interrupt")
            continue

        #  Handle CUSTOM (normal stream text from nodes)
        elif event_type == "custom":
            yield await create_chunk(index, payload, "stream")

        #  Handle END (finished flow)
        elif event_type == "end":
            yield await create_chunk(index, {"type": "done"}, "done")
            break

        #  Just yield nothing else if unknown
        else:
            print(f"Unknown event type: {event_type}")

        await asyncio.sleep(0)
        index += 1

    yield "data: [DONE]\n\n"
    
    
    
    

async def process_chat_request(request: ChatCompletionRequest):
    if request.messages:
        resp_content = "As a mock AI Assistant, I can only echo your last message:"
    else:
        resp_content = "As a mock AI Assistant, I can only echo your last message, but there wasn't one!"

    return resp_content
