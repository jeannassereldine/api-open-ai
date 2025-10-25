from typing import List
from langgraph.config import get_stream_writer
from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.messages import SystemMessage, HumanMessage
load_dotenv()

model_name = os.getenv("OLLAMA_MODEL")
llm = ChatOllama(model=model_name)


def llm_generate(messages, format) -> str:
    llm.with_structured_output(format)
    response = llm.invoke(messages)
    return response.content


def write_why_a_document_is_invalid(reasons: List[str]):
    writer = get_stream_writer()
    llm = ChatOllama(model=model_name)
    writer("Start generating a report explaining why your document is invalid.\n")
    reason_str = "\n".join(f"- {r}" for r in reasons)
    messages = [
    SystemMessage(
        content=(
            "You are an expert assistant specialized in letters of credit (LC). your role is just to tell the user what are the missed documents"
            "write a meduim paragraph"
        )
    ),
    HumanMessage(
        content=(
            f"Please find the missed documents here:\n{reason_str}\n\n"
        )
    ),
    ]


    for chunk in llm.stream(messages):
        writer(chunk.text)


def write_email_why_a_document_is_invalid(reasons: List[str]):
    writer = get_stream_writer()
    writer("Start preparing an email ready to be sent to the client\n")
    reason_str = "\n".join(f"- {r}" for r in reasons)
 

    messages = [
        SystemMessage(
            content=(
                "You are a knowledgeable assistant specialized in letters of credit. "
                "Your task is to help users clearly explain why specific trade documents are invalid. "
                "When referring to documents, use their natural names (e.g., 'certificate of origin' "
                "instead of 'CertificateOfOrigin'). Write in a professional and concise tone suitable "
                "for business email communication."
            )
        ),
        HumanMessage(
            content=(
                f"The following reasons were found for document invalidity:\n{reason_str}\n\n"
                "Please draft a medium-length professional email that politely explains these issues."
            )
        ),
    ]


    for chunk in llm.stream(messages):
        writer(chunk.text)
