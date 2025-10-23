import asyncio
from time import time


 
global id_counter 
stream_queue = asyncio.Queue()
async def process_part(data):
    
    id_counter = 0
    await stream_queue.put({
        "id": str(id_counter),
        "object": "chat.completion.chunk",
        "created": time(),
        "model": "qwen3-vl:235b-cloud",
        "choices": [{"index": id_counter, "delta": {"content": data}}],
    })
    id_counter += 1
