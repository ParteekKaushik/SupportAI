from google import genai

from app.core.config import settings
from typing import TypedDict


client = genai.Client(
    api_key=settings.google_api_key,
)


SYSTEM_INSTRUCTION = """
You are SupportAI, an AI customer support assistant.

Your responsibilities:
- Help customers with questions about products and services.
- Be polite, professional, and concise.
- If you do not know something, clearly say that you do not know.
- Never invent company policies, prices, refunds, or other business information.
- Do not claim that you performed an action unless you actually performed it.
"""


class Message(TypedDict):
    role: str
    content: str
    


def generate_response(messages: list[Message]) -> str:
    contents = [
        {
            "role": message["role"],
            "parts": [{"text": message["content"]}],
        }
        for message in messages
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config={
            "system_instruction": SYSTEM_INSTRUCTION,
        },
    )

    return response.text