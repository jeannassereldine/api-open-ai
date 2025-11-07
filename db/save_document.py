import uuid
from pydantic_mongo import AbstractRepository
from pymongo import MongoClient
from models.documents_models import DocumentsModel
import os


uri = os.getenv("URI")
# Create a repository
class DocumentsRepository(AbstractRepository[DocumentsModel]):
    class Meta:
        collection_name = "data"
        
client = MongoClient(uri)                
database = client["lc"]
repo = DocumentsRepository(database)
 
def save_document(document: DocumentsModel):
    existing_docs = list(repo.find_by({'letter_of_credit.lc_number': document.letter_of_credit.lc_number}))
    
    if existing_docs:
        print('Deleting existing document...')
        for doc in existing_docs:
            repo.delete(doc)
    repo.save(document)
    print('Document saved')

from bson import ObjectId

def get_trade_documents():
    documents = list(repo.find_by({}))  # could return Pydantic or raw dicts
    result = []
    for doc in documents:
        # If doc is a Pydantic model
        if hasattr(doc, "model_dump"):
            doc_dict = doc.model_dump()
        else:
            doc_dict = dict(doc)  # convert Mongo dict to normal dict

        # Handle MongoDB _id
        if "_id" in doc_dict:
            doc_dict["id"] = str(doc_dict["_id"])
            doc_dict.pop("_id")

        # Ensure id is string
        if "id" in doc_dict:
            doc_dict["id"] = str(doc_dict["id"])

        result.append(doc_dict)
    return result
