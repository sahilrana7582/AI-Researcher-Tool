from collections.abc import AsyncIterator
import logging

from app.ai.llm import LLMProvider

logger = logging.getLogger(__name__)


class ResearchService:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    async def research(self, query: str) -> str:
        logger.info("Research request received (query_length=%d)", len(query))

        prompt = self._build_prompt(query)

        return await self._llm.generate(prompt)

    async def research_stream(self, query: str) -> AsyncIterator[str]:
        logger.info(
            "Research stream request received (query_length=%d)",
            len(query),
        )

        prompt = self._build_prompt(query)

        async for chunk in self._llm.stream(prompt):
            yield chunk

    def _build_prompt(self, query: str) -> str:
        return (
            "Answer the following research question clearly and accurately.\n\n"
            f"Research question: {query}"
        )