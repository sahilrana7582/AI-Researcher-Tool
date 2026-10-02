import pytest

from app.ai.exceptions import LLMError
from app.ai.llm import LLMProvider
from app.services.research_service import ResearchService


class FakeLLM(LLMProvider):
    def __init__(self, response: str = "fake answer") -> None:
        self.response = response
        self.prompts: list[str] = []

    async def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


class FailingLLM(LLMProvider):
    async def generate(self, prompt: str) -> str:
        raise LLMError("provider unavailable")


async def test_research_returns_llm_answer():
    llm = FakeLLM("Kafka uses ISR replication.")

    answer = await ResearchService(llm).research("Explain ISR")

    assert answer == "Kafka uses ISR replication."


async def test_research_prompt_contains_query():
    llm = FakeLLM()

    await ResearchService(llm).research("Explain ISR")

    assert len(llm.prompts) == 1
    assert "Explain ISR" in llm.prompts[0]


async def test_research_propagates_llm_errors():
    with pytest.raises(LLMError):
        await ResearchService(FailingLLM()).research("anything")
