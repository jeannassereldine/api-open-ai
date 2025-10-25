from typing import List, Literal
from pydantic import BaseModel, Field


class Image(BaseModel):
    type: Literal['image']
    image_url_base64: str
    
class Document(BaseModel):
    type: Literal['pdf_file']
    file_data_base64: str
    

class AnalyseLCRequest(BaseModel):
    images: List[Image] = Field(default_factory=list)
    documents: List[Document] = Field(default_factory=list)
    
    
    
class ResumeRequest(BaseModel):
    thread_id: str
    interrupt_id: str
    answer: bool
    
    