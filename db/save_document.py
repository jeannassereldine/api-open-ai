from pydantic_mongo import AbstractRepository
from pymongo import MongoClient
from models.documents_models import DocumentsModel
import os
from bson import ObjectId
import uuid


uri = os.getenv("URI")


# Create a repository
class DocumentsRepository(AbstractRepository[DocumentsModel]):
    class Meta:
        collection_name = "spam"


def save_document(document: DocumentsModel):
    # Connect to database
    client = MongoClient(uri)
    database = client["lc"]
    repo = DocumentsRepository(database)
    # Save a single document
    repo.save(document)
