import logging

from app.ai.llm import LLMProvider

logger = logging.getLogger(__name__)


class ResearchService:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    async def research(self, query: str) -> str:
        logger.info("Research request received (query_length=%d)", len(query))

        prompt = (
            "Answer the following research question clearly and accurately.\n\n"
            f"Research question: {query}"
        )

        return await self._llm.generate(prompt)
