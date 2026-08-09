from google import genai

from app.core.config import settings
from app.models.message import Message

client = genai.Client(
    api_key=settings.google_api_key,
)


def generate_response(messages: list[Message], context: str) -> str:
    system_instruction = f"""
    You are SupportAI, an AI customer support assistant.

    Your responsibilities:

    - Help customers with questions about products and services.
    - Be polite, professional, and concise.
    - If you do not know something, clearly say that you do not know.
    - Never invent company policies, prices, refunds, or other business information.
    - Do not claim that you performed an action unless you actually performed it.

    Here is information retrieved from the company's knowledge base.
    Use this information to answer the user's question.

    If the answer isn't present in the context, say you don't have enough information.
    Do not invent information.

    CONTEXT:
    {context}
    """

    contents = [
        {
            "role": message["role"],
            "parts": [{"text": message["content"]}],
        }
        for message in messages
    ]

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents,
        config={
            "system_instruction": system_instruction,
        },
    )

    return response.text