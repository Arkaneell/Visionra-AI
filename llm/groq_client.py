"""
Groq LLM client wrapper.

Usage:
    from llm.groq_client import get_llm
    llm = get_llm()
"""

from functools import lru_cache
from langchain_groq import ChatGroq
from config import settings


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    """Return a cached ChatGroq instance using project settings."""
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=settings.groq_temperature,
        max_tokens=settings.groq_max_tokens,
    )
