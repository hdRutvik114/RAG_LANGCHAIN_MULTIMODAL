from functools import lru_cache

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from app.core.config import settings


@lru_cache(maxsize=1)
def get_chat_model() -> BaseChatModel:
    """Create and reuse one configured Gemini chat model."""

    return init_chat_model(
        model=settings.gemini_model,
        model_provider="google_genai",
        google_api_key=settings.gemini_api_key,
        temperature=0,
        timeout=30,
        max_retries=2,
    )