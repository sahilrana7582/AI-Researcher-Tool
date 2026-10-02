from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Send a prompt to the model and return the generated text.

        Raises:
            LLMError: If the provider call fails. Implementations must
                translate SDK and transport errors into LLMError so callers
                never depend on a specific vendor's exception types.
        """
