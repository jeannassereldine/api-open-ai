import json
from typing import List,Literal, TypedDict
from ollama import ChatResponse, chat
from pydantic import BaseModel
from models.chat_models import ChatCompletionRequest
from models.documents_models import BillOfLading, CertificateOfOrigin, CommercialInvoice, DocumentsModel, LetterOfCredit
from langgraph.graph import StateGraph, END
from services.prompt_service import prepare_messages, prompt_instruction_extract_documents_info,prompt_instruction_validate_documents


class State(TypedDict,total=False):
    is_valid: bool
    documents: DocumentsModel
    request: ChatCompletionRequest
    

required_documents = [
    "LetterOfCredit",
    "CommercialInvoice",
    "BillOfLading",
    "CertificateOfOrigin",
]

class RequiredDocuments(BaseModel):
   types: List[Literal["LetterOfCredit", "CommercialInvoice", "BillOfLading", "CertificateOfOrigin"]]

def validate_documents(state: State) -> State:
    """Validate that all required documents are present in the state."""
  
    response: ChatResponse  = chat(
        stream=False,
        model="qwen3-vl:235b-cloud",
        messages=prepare_messages(state["request"], system_instruction=prompt_instruction_validate_documents),
        format=RequiredDocuments.model_json_schema()
    )
    foundedDocuments = RequiredDocuments(**json.loads(response.message.content))
    state["is_valid"] = set(foundedDocuments.types) == set(required_documents)
    return state

def extract_documents_info(state: State) -> State:
    """Extract information from the documents and store it in the state."""
    # Placeholder for document extraction logic
    
    response: ChatResponse  = chat(
        stream=False,
        model="qwen3-vl:235b-cloud",
        think=True,
        options={'temperature': 0},
        messages=prepare_messages(state["request"], system_instruction=prompt_instruction_extract_documents_info),
        format= DocumentsModel.model_json_schema()
    )
    print("Document extraction response:", response.message.content)
    try:
        
        letterofCredit = LetterOfCredit(**json.loads(response.message.content).get("letter_of_credit", None))
        invoice = CommercialInvoice(**json.loads(response.message.content).get("commercial_invoice", None))
        landing = BillOfLading(**json.loads(response.message.content).get("bill_of_lading", None))
        certificate = CertificateOfOrigin(**json.loads(response.message.content).get("certificate_of_origin", None))
        documentsModel = DocumentsModel(
            letter_of_credit=letterofCredit,
            commercial_invoice=invoice,
            bill_of_lading=landing,
            certificate_of_origin=certificate
        )
        state["documents"] = documentsModel
    except Exception as e:
        print("Error parsing documents:", e) 
    finally:
        state["is_valid"]=False    

    state["documents"] = DocumentsModel(**json.loads(response.message.content))
    print(state["documents"])
    return state

def route_by_state(state: State) -> str:
    if state["is_valid"]:
        return 'extract_documents_info'
    else:
        return END  # In a real scenario, you might route to a different node for handling invalid cases.


def compile_graph():
    builder = StateGraph(State)
    builder.set_entry_point("validate_documents")
    builder.add_node("validate_documents", validate_documents)
    builder.add_node("extract_documents_info", extract_documents_info)  # Placeholder for document extraction logic
    builder.add_conditional_edges("validate_documents", route_by_state, {END: END, 'extract_documents_info': 'extract_documents_info'})
    builder.add_edge("extract_documents_info", END)
    return builder.compile()
