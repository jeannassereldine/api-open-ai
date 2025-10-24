from typing import List
from ollama import ChatResponse, chat
from langgraph.config import get_stream_writer

def qween_llm(messages, format)-> ChatResponse:
 
 return chat(
        stream=False,
        model="qwen2.5vl:7b",
        messages=messages,
        format=format,
    )
 
def write_why_a_document_is_invalid(reasons: List[str]):
    writer = get_stream_writer()
    print("Document invalid reason:", reasons)
    reason_str = "\n".join(f"- {r}" for r in reasons)
    stream = chat(
        stream=True,
        model="qwen2.5vl:7b",
        messages=[
            {"role": "system", "content": """You are an assistant that helps users understand why their documents are invalid, we are talking about letter of credit. 
             Don't use the document name as it's , example write certificate of origin instead of CertificateOfOrigin """},
            {"role": "user", "content": f"The following reasons were found for document invalidity:\n{reason_str}\n Please explain."}
        ]
        )
    for chunk in stream:
        if chunk.message.content:
            writer(chunk.message.content)
    
    
    