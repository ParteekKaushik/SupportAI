from app.services.conversation import (
    add_message,
    get_history,
)
from app.services.llm import generate_response
from app.services.rag.retriever import retrieve_context


def process_chat(
    conversation_id: str,
    message: str,
) -> str:
    add_message(
        conversation_id,
        "user",
        message,
    )

    history = get_history(conversation_id)
    context = retrieve_context(message)

    response = generate_response(history, context)

    add_message(
        conversation_id,
        "assistant",
        response,
    )

    return response