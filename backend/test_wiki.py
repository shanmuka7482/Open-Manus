import asyncio
from app.tool.wikipedia import WikipediaTool

async def test_wiki():
    tool = WikipediaTool()
    print("Testing WikipediaTool...")
    
    # Test 1: Normal Search
    print("\n--- Searching for 'Python (programming language)' ---")
    result = await tool.execute(query="Python (programming language)", sentences=2)
    print(result.output if result.output else result.error)

    # Test 2: Disambiguation
    print("\n--- Searching for 'Mercury' (Expect Disambiguation Error) ---")
    result = await tool.execute(query="Mercury")
    print(result.output if result.output else result.error)

if __name__ == "__main__":
    asyncio.run(test_wiki())
