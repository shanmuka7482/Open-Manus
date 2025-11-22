"""
Test script to verify the ask_user tool is properly registered and working.
Run this from the backend directory: python test_ask_user.py
"""
import asyncio
import json

from app.agent.manus import Manus
from app.logger import logger


async def test_ask_user():
    """Test the ask_user tool registration and functionality"""

    # Track if callback was called
    callback_called = False
    callback_question = None

    async def mock_callback(question: str) -> str:
        nonlocal callback_called, callback_question
        callback_called = True
        callback_question = question
        logger.info(f"🧪 Mock callback received question: {question}")
        return "blue"  # Mock user response

    # Create agent and set callback
    logger.info("🧪 Creating Manus agent...")
    agent = Manus()

    logger.info("🧪 Setting input callback...")
    agent.set_input_callback(mock_callback)

    # Check if tool is registered
    logger.info(f"🧪 Available tools: {list(agent.available_tools.tool_map.keys())}")
    logger.info(f"🧪 Total tools: {len(agent.available_tools.tool_map)}")

    # Check if ask_user is in the tools
    if "ask_user" in agent.available_tools.tool_map:
        logger.info("✅ ask_user tool is registered!")
        tool = agent.available_tools.tool_map["ask_user"]
        logger.info(
            f"🧪 Tool details: name={tool.name}, has callback={tool._input_func is not None}"
        )
    else:
        logger.error("❌ ask_user tool is NOT registered!")
        return

    # Print tool parameters to see what the LLM sees
    logger.info("🧪 Tool parameters for LLM:")
    tools_params = agent.available_tools.to_params()
    for tool_param in tools_params:
        if tool_param["function"]["name"] == "ask_user":
            logger.info(f"📋 {json.dumps(tool_param, indent=2)}")

    # Test manually calling the tool
    logger.info("🧪 Testing direct tool execution...")
    try:
        result = await agent.available_tools.execute(
            name="ask_user", tool_input={"question": "What is your favorite color?"}
        )
        logger.info(f"✅ Tool execution result: {result}")

        if callback_called:
            logger.info(f"✅ Callback was called with question: {callback_question}")
        else:
            logger.error("❌ Callback was NOT called!")
    except Exception as e:
        logger.error(f"❌ Tool execution failed: {e}")

    logger.info("\n🧪 Test complete!")


if __name__ == "__main__":
    asyncio.run(test_ask_user())
