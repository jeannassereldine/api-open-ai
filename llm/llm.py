from typing import List

from dotenv import load_dotenv
from langgraph.config import get_stream_writer
import os
# from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from models.state import State

load_dotenv()


ollama_model_name = os.getenv("OLLAMA_MODEL")
openai_model_name = os.getenv("OPEN_AI_MODEL")

llm = ChatOpenAI(model=openai_model_name, temperature=0)


def llm_generate_structured_output(messages, format:BaseModel) -> BaseModel:
    structured_llm = llm.with_structured_output(format)
    
    response = structured_llm.invoke(messages)
    print('respnse', response)
    return response



def write_why_a_document_is_invalid(state: State):
    writer = get_stream_writer()
    writer("Start generating a report explaining why this document is invalid.\n")
    reasons = state.get("non_compliance_reasons", [])
    reason_str = "\n".join(f"- {r}" for r in reasons)
    messages = [
        SystemMessage(
            content=(
                "You are an expert assistant specialized in letters of credit (LC). your role is just to tell the user what are the missed documents"
                "write a meduim paragraph"
            )
        ),
        HumanMessage(
            content=(f"Please find the missed documents here:\n{reason_str}\n\n")
        ),
    ]

    for chunk in llm.stream(messages):
        writer(chunk.text)


def write_email_why_a_document_is_invalid(state: State):
    reasons = state.get("non_compliance_reasons", [])
    writer = get_stream_writer()
    writer("Start preparing an email to send to the client explaining why his document was rejected.”\n")
    reason_str = "\n".join(f"- {r}" for r in reasons)

    messages = [
        SystemMessage(
            content=(
                "You are a knowledgeable assistant specialized in letters of credit. "
                "Your role is to help users clearly explain why specific trade documents are invalid. "
                "Use only the information explicitly provided in the input — do not add, infer, or invent any new reasons or details. "
                "When referring to documents, use their natural names (e.g., 'certificate of origin' instead of 'CertificateOfOrigin'). "
                "Write in a professional, polite, and concise tone suitable for business email communication."
            )
        ),
        HumanMessage(
            content=(
                f"The following reasons were identified for document invalidity:\n{reason_str}\n\n"
                "Please draft a medium-length professional email that politely explains these specific issues, "
                "using only the reasons provided above and without introducing any new information."
            )
        ),
    ]

    for chunk in llm.stream(messages):
        writer(chunk.text)


def generate_document_report_abou_lc(state: State):
    writer = get_stream_writer()
    writer("Start generating report.\n")
    documents_info = state["documents"].model_dump_json()
    messages = [
        SystemMessage(
            content=(
                "You are an expert assistant specialized in letters of credit (LC). "
                "Your task is to generate a clear, well-structured report about the provided letter of credit. "
                "Assume that this letter of credit is valid — do not question or evaluate its validity. "
                "Focus solely on describing its content, structure, and key characteristics in a professional and concise manner."
                "Don't ask the user any thing else and don't propose any thing."
                "generate a meduim size report"
            )
        ),
        HumanMessage(
            content=(f"Please find the documents info here:\n {documents_info}\n\n")
        ),
    ]

    for chunk in llm.stream(messages):
        writer(chunk.text)
