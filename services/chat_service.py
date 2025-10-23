import json
import time
from ollama import AsyncClient
from models.chat_models import ChatCompletionRequest, DocumentContent, ImageContent, TextContent
from typing import List
from tools.tools import pdf_base64_to_image_base64


def prepare_messages(request: ChatCompletionRequest) -> List[dict]:
    """
    Convert ChatCompletionRequest messages into a list of dicts ready for the client.
    """
    prepared_messages = []

    for msg in request.messages:
        if isinstance(msg.content, str):
            prepared_messages.append({"role": msg.role, "content": msg.content})
        else:
            for item in msg.content:
                if isinstance(item, TextContent):
                    prepared_messages.append({"role": msg.role, "content": item.text})
                elif isinstance(item, ImageContent):
                    url = item.image_url.url
                    url = url.split(",")[1] if "," in url else url
                    prepared_messages.append({
                        "role": msg.role,
                        "content": "Give a short description about the image",
                        "images": [url]
                    })
                elif isinstance(item, DocumentContent):
                    pdf_base64 = item.file.file_data
                    prepared_messages.append({
                            "role": msg.role,
                            "content": "Give a short description about these images",
                            "images": [image for image in pdf_base64_to_image_base64(pdf_base64)]
                        })
    return prepared_messages




async def _resp_async_generator(request: ChatCompletionRequest):
    client = AsyncClient()
    # print(request)
    messages = prepare_messages(request)
    print("Prepared messages:", messages)
    stream = await client.chat(
        stream=True,
        model="qwen3-vl:235b-cloud",
        messages=messages,
    )
    id = 0
    async for event in stream:
        if event.message.content:
            chunk = {
                "id": str(id),
                "object": "chat.completion.chunk",
                "created": time.time(),
                "model": "ok",
                "choices": [{"index": id, "delta": {"content": event.message.content}}],
            }
            id += 1
            yield f"data: {json.dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"



async def process_chat_request(request: ChatCompletionRequest):
    if request.messages:
        resp_content = "As a mock AI Assistant, I can only echo your last message:"
    else:
        resp_content = "As a mock AI Assistant, I can only echo your last message, but there wasn't one!"

    return resp_content
