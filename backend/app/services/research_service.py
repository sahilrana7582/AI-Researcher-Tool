from app.ai.llm import LLMProvider


class ResearchService:
    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def research(self, query: str) -> str:
        prompt = (
            "Answer the following research question clearly and accurately.\n\n"
            f"Research question: {query}"
        )

        return await self.llm.generate(prompt)