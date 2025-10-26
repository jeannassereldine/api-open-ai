from fastapi import APIRouter

from db.save_document import get_trade_documents

router = APIRouter()
  
@router.get("/trade_documents")
def get_valid_documents():
    return get_trade_documents()

