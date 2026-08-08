from typing import TypedDict


class Message(TypedDict):
    role: str
    content: str


conversations: dict[str, list[Message]] = {}


def get_history(conversation_id: str) -> list[Message]:
    return conversations.get(conversation_id, [])


def add_message(
    conversation_id: str,
    role: str,
    content: str,
) -> None:
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    conversations[conversation_id].append(
        {
            "role": role,
            "content": content,
        }
    )