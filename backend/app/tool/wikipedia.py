import wikipedia
from typing import Optional
from app.tool.base import BaseTool, ToolResult

class WikipediaTool(BaseTool):
    name: str = "wikipedia"
    description: str = (
        "Search Wikipedia for a summary of a topic. "
        "Useful for getting a quick overview or 'encyclopedic' knowledge about people, places, concepts, or events. "
        "Returns a text summary."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The topic to search for (e.g. 'Albert Einstein', 'Quantum Mechanics').",
            },
            "sentences": {
                "type": "integer",
                "description": "Number of sentences to return in the summary. Default is 3.",
                "default": 3,
            },
            "lang": {
                "type": "string",
                "description": "Language code (e.g. 'en', 'es', 'fr'). Default is 'en'.",
                "default": "en",
            },
        },
        "required": ["query"],
    }

    async def execute(self, query: str, sentences: int = 3, lang: str = "en", **kwargs) -> ToolResult:
        try:
            wikipedia.set_lang(lang)
            # Fetch summary
            summary = wikipedia.summary(query, sentences=sentences)
            # Fetch page to get the title and url
            page = wikipedia.page(query, auto_suggest=False)
            
            output_text = f"## Wikipedia Summary: {page.title}\n\n{summary}\n\n[Read more on Wikipedia]({page.url})"
            return ToolResult(output=output_text)

        except wikipedia.exceptions.DisambiguationError as e:
            # Handle ambiguous terms
            options = e.options[:5]  # Limit to first 5 options
            return ToolResult(
                error=f"The term '{query}' is ambiguous. Did you mean one of these?: {', '.join(options)}"
            )
        except wikipedia.exceptions.PageError:
            return ToolResult(error=f"Could not find a Wikipedia page for '{query}'.")
        except Exception as e:
            return ToolResult(error=f"Wikipedia tool error: {str(e)}")
