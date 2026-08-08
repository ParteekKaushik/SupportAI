from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation import (
    add_message,
    get_history,
)
from app.services.llm import generate_response


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    history = get_history(request.conversation_id)

    add_message(
        request.conversation_id,
        "user",
        request.message,
    )

    history = get_history(request.conversation_id)

    response = generate_response(history)

    add_message(
        request.conversation_id,
        "assistant",
        response,
    )

    return ChatResponse(
        conversation_id=request.conversation_id,
        response=response,
    )