from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Send a prompt to the model and return the generated text.

        Raises:
            LLMError: If the provider call fails. Implementations must
                translate SDK and transport errors into LLMError so callers
                never depend on a specific vendor's exception types.
        """

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        """
        Stream the generated response incrementally.

        The default implementation does not perform true streaming.
        It yields the complete result from generate() as a single chunk.

        Raises:
            LLMError: If generation fails, including after one or more
                chunks have already been yielded by an overriding
                implementation.
        """
        yield await self.generate(prompt)
