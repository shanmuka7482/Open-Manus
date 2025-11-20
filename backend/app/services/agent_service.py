import asyncio
import os
import json
from dataclasses import dataclass
from typing import Literal, Optional
import httpx

from app.agent.manus import Manus
from app.logger import logger
from app.config import config

IntentType = Literal["python", "presentation", "image", "website", "text"]


@dataclass
class AgentResponse:
    intent: IntentType
    output: str


class AgentService:
    """Shared gateway for Manus agent executions across CLI and API layers."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()

    def detect_intent(self, prompt: str) -> IntentType:
        """
        Detect intent with more precise matching to avoid false positives.
        Uses phrase-based matching for better accuracy.
        """
        lowered = prompt.lower()
        
        # Image: require explicit image generation requests
        image_phrases = [
            "generate image", "create image", "draw image", "make image",
            "generate picture", "create picture", "draw picture", "make picture",
            "generate photo", "create photo", "generate logo", "create logo",
            "generate illustration", "create illustration", "design image"
        ]
        if any(phrase in lowered for phrase in image_phrases):
            return "image"
        # Also check for standalone image keywords at start or with action verbs
        if any(word in lowered.split()[:3] for word in ["image", "picture", "photo", "logo", "illustration"]):
            if any(action in lowered for action in ["generate", "create", "draw", "make", "design"]):
                return "image"
        
        # Presentation: require explicit presentation/slides requests
        presentation_phrases = [
            "create presentation", "generate presentation", "make presentation",
            "create slides", "generate slides", "make slides", "create ppt",
            "generate ppt", "make ppt", "powerpoint", "power point"
        ]
        if any(phrase in lowered for phrase in presentation_phrases):
            return "presentation"
        if any(word in lowered.split()[:3] for word in ["presentation", "slides", "ppt"]):
            if any(action in lowered for action in ["create", "generate", "make"]):
                return "presentation"
        
        # Website: require explicit website/webpage creation
        website_phrases = [
            "create website", "generate website", "make website", "build website",
            "create webpage", "generate webpage", "make webpage", "create landing page",
            "generate landing page", "make landing page"
        ]
        if any(phrase in lowered for phrase in website_phrases):
            return "website"
        if any(word in lowered.split()[:3] for word in ["website", "webpage", "landing page"]):
            if any(action in lowered for action in ["create", "generate", "make", "build"]):
                return "website"
        
        # Python: require explicit code/script creation or execution
        python_phrases = [
            "create python", "write python", "generate python", "make python",
            "python script", "python code", "python file", "python program",
            "write script", "create script", "write code", "create code",
            "execute python", "run python", "python function"
        ]
        if any(phrase in lowered for phrase in python_phrases):
            return "python"
        # Check for "python" as first word or with action verbs
        words = lowered.split()
        if len(words) > 0 and words[0] == "python":
            return "python"
        if "python" in lowered and any(action in lowered for action in ["create", "write", "generate", "make", "execute", "run"]):
            return "python"
        
        # Default to text for general questions and unclear intents
        return "text"

    async def _direct_openrouter_fallback(self, prompt: str, intent: IntentType) -> str:
        """Direct OpenRouter API fallback when agent fails due to auth issues"""
        try:
            llm_config = config.llm.get("default")
            if not llm_config:
                return "Error: No LLM configuration found"
            
            api_key = llm_config.api_key
            base_url = llm_config.base_url or "https://openrouter.ai/api/v1"
            model = llm_config.model or "meta-llama/llama-3.3-70b-instruct:free"
            
            # Check for environment variable as fallback
            env_key = os.getenv("OPENROUTER_API_KEY", "")
            if env_key and env_key.startswith("sk-or-v1-"):
                api_key = env_key
            elif not api_key or api_key == "YOUR_API_KEY" or not api_key.startswith("sk-or-v1-"):
                if env_key:
                    api_key = env_key
                else:
                    return "Error: No valid OpenRouter API key found. Please set OPENROUTER_API_KEY environment variable or update config.toml. Get a free key at: https://openrouter.ai/keys"
            
            if not api_key or not api_key.startswith("sk-or-v1-"):
                return "Error: Invalid OpenRouter API key format. Keys should start with 'sk-or-v1-'. Get a free key at: https://openrouter.ai/keys"
            
            # Format prompt based on intent
            system_msg = self._get_fallback_system_message(intent)
            messages = []
            if system_msg:
                messages.append({"role": "system", "content": system_msg})
            messages.append({"role": "user", "content": prompt})
            
            # Direct API call with proper OpenRouter headers
            async with httpx.AsyncClient(timeout=60.0) as client:
                url = f"{base_url.rstrip('/')}/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://open-manus-blue.vercel.app",
                    "X-Title": "OpenManus",
                }
                
                response = await client.post(
                    url,
                    headers=headers,
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": 0.0,
                        "max_tokens": 2048,
                    },
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
                elif response.status_code == 401:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", "Authentication failed")
                    return f"Authentication Error: {error_msg}. Please check your OpenRouter API key at https://openrouter.ai/keys"
                else:
                    return f"API Error {response.status_code}: {response.text[:200]}"
        except Exception as e:
            logger.warning(f"⚠️ Direct OpenRouter fallback failed: {e}")
            return f"Fallback error: {str(e)}"
    
    def _get_fallback_system_message(self, intent: IntentType) -> str:
        """Get system message for fallback based on intent"""
        messages = {
            "python": "You are a Python expert. Provide clean, runnable Python code with brief explanations.",
            "presentation": "You are a presentation expert. Provide a structured outline for slides with titles and bullet points.",
            "image": "You are an image generation expert. Describe the image concept clearly.",
            "website": "You are a web developer. Provide complete HTML/CSS/JS code.",
            "text": "You are a helpful assistant. Provide clear, concise answers.",
        }
        return messages.get(intent, messages["text"])

    async def process_prompt(
        self,
        prompt: str,
        intent: Optional[IntentType] = None,
        use_fallback: bool = True,
    ) -> AgentResponse:
        cleaned_prompt = prompt.strip()
        if not cleaned_prompt:
            raise ValueError("Prompt cannot be empty.")

        resolved_intent = intent or self.detect_intent(cleaned_prompt)
        formatted_prompt = self._format_prompt(cleaned_prompt, resolved_intent)

        agent = None
        try:
            async with self._lock:
                agent = Manus()
                logger.info(f"🚀 Manus handling '{resolved_intent}' request via AgentService.")
                result = await agent.run(formatted_prompt)
                logger.info("✅ Manus execution finished.")
                return AgentResponse(intent=resolved_intent, output=result)
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"⚠️ Agent execution failed: {error_msg}")
            
            # Extract root cause from nested exceptions
            root_cause = e
            while hasattr(root_cause, "__cause__") and root_cause.__cause__:
                root_cause = root_cause.__cause__
            
            root_error_msg = str(root_cause)
            root_error_type = type(root_cause).__name__
            
            # If authentication error and fallback enabled, try direct API call
            if use_fallback and ("AuthenticationError" in root_error_type or "401" in root_error_msg or "403" in root_error_msg or "User not found" in root_error_msg):
                logger.info("🔄 Attempting direct OpenRouter API fallback due to authentication error...")
                try:
                    result = await self._direct_openrouter_fallback(cleaned_prompt, resolved_intent)
                    if result and not result.startswith("Error:") and not result.startswith("Authentication Error:"):
                        logger.info("✅ Fallback API call succeeded")
                        return AgentResponse(intent=resolved_intent, output=result)
                    else:
                        # Fallback also failed, provide helpful error
                        raise ValueError(
                            f"{result}\n\n"
                            "To fix this:\n"
                            "1. Get a free API key from https://openrouter.ai/keys\n"
                            "2. Update backend/config/config.toml with your key:\n"
                            "   [llm]\n"
                            "   api_key = \"sk-or-v1-YOUR_KEY_HERE\"\n"
                            "3. Or set OPENROUTER_API_KEY environment variable"
                        )
                except Exception as fallback_error:
                    logger.error(f"❌ Fallback also failed: {fallback_error}")
                    raise ValueError(
                        f"Both agent and fallback failed.\n"
                        f"Original error: {root_error_msg}\n"
                        f"Fallback error: {str(fallback_error)}\n\n"
                        "Please get a valid OpenRouter API key from https://openrouter.ai/keys"
                    ) from e
            
            # For other errors, raise normally
            if "AuthenticationError" in root_error_type or "authentication" in root_error_msg.lower():
                raise ValueError(
                    f"Authentication failed: {root_error_msg}. "
                    "Please check your LLM API key in backend/config/config.toml. "
                    "Get a free key from: https://openrouter.ai/keys"
                ) from e
            elif "api_key" in root_error_msg.lower() or "api key" in root_error_msg.lower():
                raise ValueError(
                    f"API key error: {root_error_msg}. "
                    "Please configure your LLM API key in backend/config/config.toml"
                ) from e
            else:
                raise RuntimeError(f"Agent execution failed: {root_error_msg} (Type: {root_error_type})") from e
        finally:
            # Ensure cleanup happens even on errors
            if agent:
                try:
                    await agent.cleanup()
                except Exception as cleanup_error:
                    logger.warning(f"⚠️ Error during agent cleanup: {cleanup_error}")

    def _format_prompt(self, prompt: str, intent: IntentType) -> str:
        intent_templates = {
            "python": (
                "You are a senior Python engineer. Write or update Python files as requested.\n"
                "Use the python_execute tool for running snippets when needed and explain outputs succinctly.\n\n"
                "Task:\n{prompt}"
            ),
            "presentation": (
                "Create a concise but informative presentation outline and then use the create_presentation tool\n"
                "to store the PPTX under the workspace directory. Explain the slide strategy before calling the tool.\n\n"
                "Topic:\n{prompt}"
            ),
            "image": (
                "You can call the generate_image tool (requires filename ending with .png).\n"
                "Craft a vivid, detailed prompt and save the resulting image under the workspace directory.\n"
                "Describe the concept first, then trigger the tool call.\n\n"
                "Image brief:\n{prompt}"
            ),
            "website": (
                "Act as a full-stack developer. Produce HTML/CSS/JS necessary for the requested experience.\n"
                "If appropriate, use the StrReplaceEditor tool to write files under workspace/.\n\n"
                "Specification:\n{prompt}"
            ),
            "text": (
                "Provide a thoughtful, well-structured response for the following request.\n\n{prompt}"
            ),
        }
        return intent_templates[intent].format(prompt=prompt)


agent_service = AgentService()

