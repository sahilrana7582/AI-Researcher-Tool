from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from app.ai.llm_exception import LLMError
from app.ai.llm import LLMProvider


class LangChainProvider(LLMProvider):
    def __init__(
        self,
        model: Runnable,
        exceptions: tuple[type[Exception], ...],
    ):
        self.chain = model | StrOutputParser()
        self.exceptions = exceptions

    async def generate(self, prompt: str) -> str:
        try:
            result = await self.chain.ainvoke(prompt)
        except self.exceptions as exc:
            raise LLMError("LLM provider call failed") from exc

        if not result:
            raise LLMError("LLM provider returned empty output")

        return result