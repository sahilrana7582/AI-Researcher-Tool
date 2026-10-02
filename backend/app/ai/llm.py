from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Generate a text response from the given prompt.

        Implementations must asynchronously send the prompt to an
        LLM provider and return the generated response as a string.
        """
        pass