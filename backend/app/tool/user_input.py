import asyncio
from typing import Any, Callable, Optional

from app.tool.base import BaseTool


class UserInputTool(BaseTool):
    name: str = "ask_user"
    description: str = (
        "Ask the user a question and wait for their response. "
        "Use this tool when you need clarification, confirmation, or additional information from the user."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question to ask the user.",
            }
        },
        "required": ["question"],
    }

    _input_func: Optional[Callable[[str], Any]] = None

    def __init__(self, input_func: Optional[Callable[[str], Any]] = None, **data):
        super().__init__(**data)
        self._input_func = input_func

    async def execute(self, question: str, **kwargs) -> Any:
        if self._input_func:
            return await self._input_func(question)

        # Default to CLI input if no callback provided
        print(f"\n🤖 Manus asks: {question}")
        return await asyncio.to_thread(input, "You: ")
