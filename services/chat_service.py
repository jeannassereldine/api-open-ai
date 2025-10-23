from graph.graph_excecutor import compile_graph
from models.chat_models import ChatCompletionRequest
from models.documents_models import DocumentsModel

graph = compile_graph()

async def _resp_async_generator(request: ChatCompletionRequest):
    # client = AsyncClient()
    # print(request)
    state = {"request": request, "is_valid": False} 
 
    graph.invoke(state)
    # stream = await client.chat(
    #     stream=True,
    #     model="qwen3-vl:235b-cloud",
    #     messages=messages,
    #     format=DocumentsModel.model_json_schema()
    # )
    # id = 0
    # async for event in stream:
    #     if event.message.content:
    #         chunk = {
    #             "id": str(id),
    #             "object": "chat.completion.chunk",
    #             "created": time.time(),
    #             "model": "ok",
    #             "choices": [{"index": id, "delta": {"content": event.message.content}}],
    #         }
    #         id += 1
    #         yield f"data: {json.dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"



async def process_chat_request(request: ChatCompletionRequest):
    if request.messages:
        resp_content = "As a mock AI Assistant, I can only echo your last message:"
    else:
        resp_content = "As a mock AI Assistant, I can only echo your last message, but there wasn't one!"

    return resp_content
