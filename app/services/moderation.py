from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def analyze_content(content: str) -> dict:
    """
    Отправляет контент в OpenAI и получает оценку токсичности.
    Возвращает словарь с результатами анализа.
    """
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a content moderation AI. 
                Analyze the given text and return a JSON with:
                - is_toxic (boolean)
                - toxicity_score (float 0.0 to 1.0)
                - categories (object with boolean fields: hate, harassment, spam, violence)
                Respond ONLY with valid JSON, no markdown."""
            },
            {
                "role": "user",
                "content": content
            }
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    import json
    result = json.loads(response.choices[0].message.content)
    return result