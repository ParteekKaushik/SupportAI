from app.models.message import Message


conversations: dict[str, list[Message]] = {}


def get_history(
    conversation_id: str,
) -> list[Message]:
    return conversations.get(
        conversation_id,
        [],
    )


def add_message(
    conversation_id: str,
    role: Message["role"],
    content: str,
) -> None:
    conversations.setdefault(
        conversation_id,
        [],
    ).append(
        {
            "role": role,
            "content": content,
        }
    )