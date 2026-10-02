import asyncio
from dotenv import load_dotenv

from app.ai.factory import create_llm_provider
from app.core.config import get_settings

load_dotenv()

async def main():
    settings = get_settings()

    llm = create_llm_provider(settings)

    result = await llm.generate("Who is Mia Khalifa..?")

    print(result)


asyncio.run(main())