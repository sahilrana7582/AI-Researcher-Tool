from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from app.ai.exceptions import LLMError
from app.ai.llm import LLMProvider


class LangChainProvider(LLMProvider):
    """LLMProvider backed by a LangChain chat model.

    Only the exception types in `handled_errors` are translated into LLMError.
    Anything else is a bug and is allowed to propagate.
    """

    def __init__(
        self,
        model: Runnable,
        handled_errors: tuple[type[Exception], ...],
    ) -> None:
        self._chain = model | StrOutputParser()
        self._handled_errors = handled_errors

    async def generate(self, prompt: str) -> str:
        try:
            text = await self._chain.ainvoke(prompt)
        except self._handled_errors as exc:
            raise LLMError(f"LLM provider call failed: {type(exc).__name__}") from exc

        if not text.strip():
            raise LLMError("LLM provider returned empty output")

        return text
