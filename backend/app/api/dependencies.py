from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.ai.factory import create_llm_provider
from app.ai.llm import LLMProvider
from app.core.config import get_settings
from app.services.research_service import ResearchService


@lru_cache
def get_llm_provider() -> LLMProvider:
    return create_llm_provider(get_settings())


def get_research_service(
    llm: Annotated[LLMProvider, Depends(get_llm_provider)],
) -> ResearchService:
    return ResearchService(llm)


ResearchServiceDep = Annotated[ResearchService, Depends(get_research_service)]
