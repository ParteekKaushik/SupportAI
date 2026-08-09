from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import process_chat


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = process_chat(
        conversation_id=request.conversation_id,
        message=request.message,
    )

    return ChatResponse(
        conversation_id=request.conversation_id,
        response=response,
    )