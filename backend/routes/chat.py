from fastapi import APIRouter

from backend.schemas.chatSchema import ChatRequest, ChatResponse
from backend.services.llm import process_chat_request    

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@chat_router.post("/")
async def chat_endpoint(request: ChatRequest):
    # process the chat request and send response
    response = process_chat_request(request.query)
    return ChatResponse(status=True, response=response)