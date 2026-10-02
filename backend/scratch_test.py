import asyncio

from app.ai.llm import LLMProvider
from app.services.research_service import ResearchService


class EchoLLM(LLMProvider):
    async def generate(self, prompt: str) -> str:
        return "echo: " + prompt


async def main():
    service = ResearchService(EchoLLM())

    result = await service.research("test")

    print(result)


asyncio.run(main())