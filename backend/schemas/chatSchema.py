from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    
class ChatResponse(BaseModel):
    status: bool
    response: str