from app.services.conversation import (
    add_message,
    get_history,
)
from app.services.llm import generate_response


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

    response = generate_response(history)

    add_message(
        conversation_id,
        "assistant",
        response,
    )

    return response