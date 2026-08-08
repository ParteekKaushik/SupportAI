from google import genai

from app.core.config import settings


client = genai.Client(
    api_key=settings.google_api_key,
)


def generate_response(message: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message,
    )

    return response.text