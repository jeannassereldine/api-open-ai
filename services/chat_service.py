import asyncio
from datetime import time
import json
from graph.graph_excecutor import compile_graph
from typing import AsyncGenerator, Literal
from models.chat_models import AnalyseLCRequest, ResumeRequest
graph = compile_graph()
import asyncio
import json
from typing import AsyncGenerator
import asyncio
import json
from typing import AsyncGenerator
from datetime import datetime
from langgraph.types import Command
import uuid

async def _resp_async_generator(req:AnalyseLCRequest | ResumeRequest) -> AsyncGenerator[str, None]:
    """
    Async generator to stream chunks from LangGraph including interrupts.
    """
    thread_id =  str(uuid.uuid4()) if  isinstance(req,AnalyseLCRequest)  else req.thread_id
    config = {"configurable": {"thread_id":  thread_id}}
    input =   ({"request": req, "is_valid": False} if  isinstance(req,AnalyseLCRequest) 
             else  Command(resume=req.answer))
    index = 0

    for event_type, payload in graph.stream(
        input=input, stream_mode=["custom", "updates"], config=config
    ):
        # Handle INTERRUPT (pause and ask user)
        if event_type == "updates" and "__interrupt__" in payload:
            interrupt_obj = payload["__interrupt__"][0]
            question = interrupt_obj.value.get("question")
            interrupt_id = interrupt_obj.id
            yield f"event: interrupt\ndata: {json.dumps({ 'question': question, 'interrupt_id': interrupt_id , 'thread_id':thread_id })}\n\n"
            continue

        # Handle CUSTOM (normal stream text from nodes)
        elif event_type == "custom":
            yield f"event: message\ndata: {json.dumps(payload)}\n\n"

        # Handle END (finished flow)
        elif event_type == "end":
            yield f"event: message\ndata: {json.dumps(payload)}\n\n"
            break

        # Just yield nothing else if unknown
        else:
            print(f"Unknown event type: {event_type}")
        # let you send stream to the client
        await asyncio.sleep(0)
        index += 1

    
    
    
    
    
