from typing import List, Optional, Union, Literal
from pydantic import BaseModel


class TextContent(BaseModel):
    type: Literal["text"]
    text: str

class  ImageUrl(BaseModel):
    url: str

class ImageContent(BaseModel):
    type: Literal["image_url"]
    image_url: ImageUrl

class FileContent(BaseModel):
    file_data: str
    
class DocumentContent(BaseModel):
    type: Literal["file"]
    file: FileContent


class Message(BaseModel):
    role: str
    content: Union[str, List[Union[TextContent, ImageContent, DocumentContent]]]


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "mock-gpt-model"
    messages: List[Message]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.1
    stream: Optional[bool] = False
