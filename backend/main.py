import asyncio
from app.logger import logger
from app.services.agent_service import agent_service


async def main():
    try:
        prompt = input("Enter your prompt: ")
        if not prompt.strip():
            logger.warning("Empty prompt provided.")
            return

        logger.warning("Processing your request via Manus agent...")
        result = await agent_service.process_prompt(prompt)
        logger.info("Request processing completed.")
        print(result.output)
    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")


if __name__ == "__main__":
    asyncio.run(main())
