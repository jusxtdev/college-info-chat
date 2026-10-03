from fastapi import APIRouter

from schemas.chatSchema import ChatRequest, ChatResponse
from services.llm import process_chat_request

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@chat_router.post("/")
async def chat_endpoint(request: ChatRequest):
    response = process_chat_request(request.query)
    return ChatResponse(status=True, response=response)