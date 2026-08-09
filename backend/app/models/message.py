from typing import Literal, TypedDict


class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str