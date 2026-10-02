import openai
from langchain_openai import ChatOpenAI

from app.ai.langchain_provider import LangChainProvider
from app.ai.llm import LLMProvider
from app.core.config import Settings


def create_llm_provider(settings: Settings) -> LLMProvider:
    model = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.llm_api_key,
        timeout=settings.llm_timeout_seconds,
        max_retries=settings.llm_max_retries,
    )

    return LangChainProvider(
        model=model,
        handled_errors=(openai.OpenAIError,),
    )
