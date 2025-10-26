from pydantic_mongo import AbstractRepository
from pymongo import MongoClient
from models.documents_models import DocumentsModel
import os


uri = os.getenv("URI")
# Create a repository
class DocumentsRepository(AbstractRepository[DocumentsModel]):
    class Meta:
        collection_name = "spam"
        
client = MongoClient(uri)                
database = client["lc"]
repo = DocumentsRepository(database)
 
def save_document(document: DocumentsModel):
    # Save a single document
    repo.save(document)

def get_trade_documents():
    documents = list(repo.find_by({}))
    return [doc.model_dump() for doc in documents]