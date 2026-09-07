from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.openai_api_key
)


def ask_llm(prompt: str) -> str:
    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
    )

    return response.output_text
