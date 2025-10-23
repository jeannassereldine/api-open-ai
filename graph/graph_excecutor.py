import asyncio
import json
from time import time
from typing import List, Literal, TypedDict
from ollama import ChatResponse, chat
from pydantic import BaseModel
from business.rules import validate_letter_of_credit
from llm.qween_llm import qween_llm
from models.chat_models import ChatCompletionRequest
from models.documents_models import (
    BillOfLading,
    CertificateOfOrigin,
    CommercialInvoice,
    DocumentsModel,
    LetterOfCredit,
)
from langgraph.graph import StateGraph, END
from services.stream_service import process_part
from services.prompt_service import (
    prepare_messages,
    prompt_instruction_extract_documents_info,
    prompt_instruction_validate_documents,
)




class State(TypedDict, total=False):
    is_valid: bool
    documents: DocumentsModel
    request: ChatCompletionRequest
    non_compliance_reasons: List[str]


required_documents = [
    "LetterOfCredit",
    "CommercialInvoice",
    "BillOfLading",
    "CertificateOfOrigin",
]


class RequiredDocuments(BaseModel):
    types: List[
        Literal[
            "LetterOfCredit", "CommercialInvoice", "BillOfLading", "CertificateOfOrigin"
        ]
    ]


async def  validate_documents(state: State) -> State:
    """Validate that all required documents are present in the state."""
    
    print('Validating provided documents...')
    response: ChatResponse = qween_llm(
        prepare_messages(state["request"], prompt_instruction_validate_documents),
        RequiredDocuments.model_json_schema(),
    )
    await process_part("Starting document validation...\n")
    foundedDocuments = RequiredDocuments(**json.loads(response.message.content))
    state["is_valid"] = set(foundedDocuments.types) == set(required_documents)
    msg = "You have provided all the needed document" if  state["is_valid"] == True else "some documents are missing or invalid"
    await process_part(msg + "\n")
    return state


async def extract_documents_info(state: State) -> State:
    """Extract information from the documents and store it in the state."""
    await process_part('Trying extracting informations from documents' + "\n")
    response = qween_llm(
        prepare_messages(state["request"], prompt_instruction_extract_documents_info),
        DocumentsModel.model_json_schema(),
    )
    try:

        letterofCredit = LetterOfCredit(
            **json.loads(response.message.content).get("letter_of_credit", None)
        )
        
        print('letterofCredit:', letterofCredit)
        
        invoice = CommercialInvoice(
            **json.loads(response.message.content).get("commercial_invoice", None)
        )
        landing = BillOfLading(
            **json.loads(response.message.content).get("bill_of_lading", None)
        )
        certificate = CertificateOfOrigin(
            **json.loads(response.message.content).get("certificate_of_origin", None)
        )
        documentsModel = DocumentsModel(
            letter_of_credit=letterofCredit,
            commercial_invoice=invoice,
            bill_of_lading=landing,
            certificate_of_origin=certificate,
        )
        state["documents"] = documentsModel
    except Exception as e:
        print("Error parsing documents:", e)
    finally:
        state["is_valid"] = False

    state["documents"] = DocumentsModel(**json.loads(response.message.content))
    state["is_valid"] = True
    await process_part('Documents information extracted successfully' + "\n")
    return state


def validate_information(state: State) -> State:
    """Validate the extracted information from the documents."""
    result = validate_letter_of_credit(state["documents"])
    state["is_valid"] = result.is_compliant
    state["non_compliance_reasons"] = result.reasons
    print('----------------------------------------')
    print("Validation result:", result)
    return state

def generate_report(state: State) -> State:
    """Generate a report based on the validated documents."""
    # For simplicity, let's just print a message.
    print("Generating report based on the documents")
    
    
    
    return state

def handle_invalide_documents(state: State) -> State:
    """Handle the case where documents are invalid."""
    print("Handling invalid documents.")
    return state


def route_by_state(state: State) -> str:
    if state["is_valid"]:
        return "ok"
    else:
        return 'invalide_documents'  # In a real scenario, you might route to a different node for handling invalid cases.


def compile_graph():
    builder = StateGraph(State)
    builder.set_entry_point("validate_documents")
    builder.add_node("validate_documents", validate_documents)
    builder.add_node("extract_documents_info", extract_documents_info)
    builder.add_node("validate_information", validate_information)
    builder.add_node("generate_report", generate_report)
    builder.add_node("handle_invalide_documents", handle_invalide_documents)
   
    builder.add_conditional_edges(
        "validate_documents",
        route_by_state,
        {'invalide_documents': 'handle_invalide_documents', "ok": "extract_documents_info"},
    )

    builder.add_conditional_edges(
        "extract_documents_info",
        route_by_state,
        {'invalide_documents': 'handle_invalide_documents', "ok": "validate_information"},
    )
    
    builder.add_conditional_edges(
        "validate_information",
        route_by_state,
        {'invalide_documents': 'handle_invalide_documents', "ok": "generate_report"})
    

    builder.add_edge("generate_report", END)
    builder.add_edge("handle_invalide_documents", END)
    return builder.compile()
