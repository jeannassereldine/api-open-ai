from ollama import ChatResponse, chat

def qween_llm(messages, format)-> ChatResponse:
 
 return chat(
        stream=False,
        model="qwen3-vl:235b-cloud",
        messages=messages,
        format=format
    )