import json
from typing import List, Literal
from pydantic import BaseModel
from business.rules import validate_letter_of_credit
from db.save_images import save_images
from db.save_document import save_document
from llm.llm import (
    generate_document_report_abou_lc,
    llm_generate_structured_output,
    write_email_why_a_document_is_invalid,
    write_why_a_document_is_invalid,
)
from models.chat_models import AnalyseLCRequest
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from models.documents_models import DocumentsModel
  
from langgraph.graph import StateGraph, END
from langgraph.config import get_stream_writer

from models.state import State
from services.prompt_service import (
    prepare_messages,
    prompt_instruction_extract_documents_info,
    prompt_instruction_validate_documents,
)

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


def validate_documents(state: State) -> State:
    """Validate that all required documents are present in the state."""
    writer = get_stream_writer()
    messages, _ =  prepare_messages(state["request"], prompt_instruction_validate_documents)
    response = llm_generate_structured_output(
       messages,
       RequiredDocuments,
    )
    writer("Checking for required documents...\n")

    foundedDocuments = response
    is_valid = set(foundedDocuments.types) == set(required_documents)
    state["is_valid"] = is_valid

    if not is_valid:
        missing_docs = set(required_documents) - set(foundedDocuments.types)
        non_compliance_reasons = state.get("non_compliance_reasons", [])
        non_compliance_reasons.append(
            f"Missing required documents: {', '.join(missing_docs)}"
        )
        state["non_compliance_reasons"] = non_compliance_reasons
        writer("Missing required documents.\n") 
    else:
        writer("All required documents are present.\n")
    return state


def extract_documents_info(state: State) -> State:
    """Extract information from the documents and store it in the state."""
    writer = get_stream_writer()
    writer("Extracting information from documents...\n")
    messages,images = prepare_messages(state["request"], prompt_instruction_extract_documents_info)
    state['images'] = images
    try:
        documentsModel = llm_generate_structured_output(messages, DocumentsModel)
        state["documents"] = documentsModel
        state["is_valid"] = True
        print('documentsModel', documentsModel)
    except Exception as e:
        print("Error parsing documents:", e)
        state["is_valid"] = False
    
    writer("Documents information extracted successfully" + "\n")
    return state


def validate_information(state: State) -> State:
    """Validate the extracted information from the documents."""
    writer = get_stream_writer()
    writer("Checking business rules\n")
    result = validate_letter_of_credit(state["documents"])
    state["is_valid"] = result.is_compliant
    state["non_compliance_reasons"] = result.reasons
    return state


def generate_report(state: State) -> State:
    """Generate a report based on the validated documents."""
    # For simplicity, let's just print a message.
    writer = get_stream_writer()
    writer("Generating report and saving data...\n")
    generate_document_report_abou_lc(state)
    paths = save_images(state)
    state['documents'].images = paths
    save_document(state['documents'])
    writer("\nReport generated and data saved successfully.\nValidation complete.\n")
    return state

def handle_invalid_documents(state: State) -> State:
    """Handle the case where documents are invalid."""
    write_why_a_document_is_invalid(state)
    return state


def ask_to_write_email_node(
    state: State,
) -> Command[Literal["write_email", "__end__"]]:
    # Pause execution; payload shows up under result["__interrupt__"]
    print("Asking user for email sending approval...")
    is_approved = interrupt(
        {
            "question": "Would you like to prepare an email explaining the reason these documents was rejected?",
        }
    )

    # Route based on the response
    if is_approved == True:
        return Command(goto="write_email")  # Runs after the resume payload is provided
    else:
        return Command(goto=END)


def write_email_node(state: State) -> State:
    
    write_email_why_a_document_is_invalid(state)
    return state


def route_by_state(state: State) -> str:
    if state["is_valid"]:
        return "ok"
    else:
        return "invalid_documents"  # In a real scenario, you might route to a different node for handling invalid cases.


def compile_graph():
    builder = StateGraph(State)
    builder.set_entry_point("validate_documents")
    builder.add_node("validate_documents", validate_documents)
    builder.add_node("extract_documents_info", extract_documents_info)
    builder.add_node("validate_information", validate_information)
    builder.add_node("generate_report", generate_report)
    builder.add_node("handle_invalid_documents", handle_invalid_documents)
    builder.add_node("ask_to_write_email", ask_to_write_email_node)
    builder.add_node("write_email", write_email_node)

    builder.add_conditional_edges(
        "validate_documents",
        route_by_state,
        {
            "invalid_documents": "handle_invalid_documents",
            "ok": "extract_documents_info",
        },
    )

    builder.add_conditional_edges(
        "extract_documents_info",
        route_by_state,
        {
            "invalid_documents": "handle_invalid_documents",
            "ok": "validate_information",
        },
    )

    builder.add_conditional_edges(
        "validate_information",
        route_by_state,
        {"invalid_documents": "handle_invalid_documents", "ok": "generate_report"},
    )

    builder.add_edge("generate_report", END)
    builder.add_edge("handle_invalid_documents", "ask_to_write_email")
    builder.add_edge("ask_to_write_email", END)
    builder.add_edge("write_email", END)

    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)
