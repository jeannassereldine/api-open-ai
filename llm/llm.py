from typing import List
from ollama import ChatResponse, chat
from langgraph.config import get_stream_writer
from dotenv import load_dotenv
import os

load_dotenv()

model = os.getenv('OLLAMA_MODEL')

def llm_generate(messages, format) -> ChatResponse:
    return chat(
        stream=False,
        model=model,
        messages=messages,
        format=format)


def write_why_a_document_is_invalid(reasons: List[str]):
    writer = get_stream_writer()
    print("Document invalid reason:", reasons)
    writer("Start generating a report about why you document is invalid\n")
    reason_str = "\n".join(f"- {r}" for r in reasons)
    stream = chat(
        stream=True,
        model=model,
        messages=[
            {
                "role": "system",
                "content": """You are an assistant that helps users understand why their documents are invalid, we are talking about letter of credit. 
             Don't use the document name as it's , example write certificate of origin instead of CertificateOfOrigin """,
            },
            {
                "role": "user",
                "content": f"The following reasons were found for document invalidity:\n{reason_str}\n Please explain.",
            },
        ],
    )
    for chunk in stream:
        if chunk.message.content:
            writer(chunk.message.content)


def write_email_why_a_document_is_invalid(reasons: List[str]):
    writer = get_stream_writer()
    writer("Start preparing an email ready to be sent to the client")
    reason_str = "\n".join(f"- {r}" for r in reasons)
    stream = chat(
        stream=True,
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a knowledgeable assistant specialized in letters of credit. "
                    "Your task is to help users clearly explain why specific trade documents are invalid. "
                    "When referring to documents, use their natural names (e.g., 'certificate of origin' "
                    "instead of 'CertificateOfOrigin'). Write in a professional and concise tone suitable for business email communication."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"The following reasons were found for document invalidity:\n{reason_str}\n\n"
                    "Please draft a medium-length professional email that politely explains these issues."
                ),
            },
        ],
    )
    for chunk in stream:
        if chunk.message.content:
            writer(chunk.message.content)
