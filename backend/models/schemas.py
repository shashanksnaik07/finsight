from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = "default"

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list
    benchmark: Optional[dict] = None

class DocumentResponse(BaseModel):
    file_name: str
    metadata: dict
    calculated_summary: dict
    benchmark: dict
    message: str