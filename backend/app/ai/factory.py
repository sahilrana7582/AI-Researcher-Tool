import openai
from langchain_openai import ChatOpenAI

from app.ai.llm import LLMProvider
from app.ai.langchain_provider import LangChainProvider


def create_llm_provider(settings) -> LLMProvider:
    model = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.llm_api_key.get_secret_value(),
        timeout=settings.llm_timeout,
        max_retries=settings.llm_max_retries,
    )

    return LangChainProvider(
        model=model,
        exceptions=(openai.OpenAIError,),
    )