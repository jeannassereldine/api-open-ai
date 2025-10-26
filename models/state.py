from typing import List, TypedDict

from models.chat_models import AnalyseLCRequest
from models.documents_models import DocumentsModel


class State(TypedDict, total=False):
    is_valid: bool
    documents: DocumentsModel
    request: AnalyseLCRequest
    non_compliance_reasons: List[str]
    images:List[str]