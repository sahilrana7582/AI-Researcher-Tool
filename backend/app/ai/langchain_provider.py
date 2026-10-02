from collections.abc import AsyncIterator

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
            raise LLMError(
                f"LLM provider call failed: {type(exc).__name__}"
            ) from exc

        if not text.strip():
            raise LLMError("LLM provider returned empty output")

        return text

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        has_content = False

        try:
            async for chunk in self._chain.astream(prompt):
                if not chunk:
                    continue

                # Whitespace-only chunks ("\n\n", " ") are real tokens that
                # carry formatting, so they are forwarded, not dropped.
                if chunk.strip():
                    has_content = True

                yield chunk

        except self._handled_errors as exc:
            raise LLMError(
                f"LLM provider stream failed: {type(exc).__name__}"
            ) from exc

        if not has_content:
            raise LLMError("LLM provider returned empty output")