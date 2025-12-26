from app.tool.base import BaseTool


_TERMINATE_DESCRIPTION = """Terminate the interaction when the request is met OR if the assistant cannot proceed further with the task.
When you have finished all the tasks, call this tool to end the work."""


class Terminate(BaseTool):
    name: str = "terminate"
    description: str = _TERMINATE_DESCRIPTION
    parameters: dict = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "The finish status of the interaction.",
                "enum": ["success", "failure"],
            },
            "summary": {
                "type": "string",
                "description": "A comprehensive Markdown summary of the session, detailing what was accomplished and any key findings.",
            },
            "follow_up_suggestions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of 3 suggested follow-up questions or actions for the user.",
            }
        },
        "required": ["status"],
    }

    async def execute(self, status: str, summary: str = "", follow_up_suggestions: list[str] = None) -> str:
        """Finish the current execution"""
        import os
        from pathlib import Path
        
        result_msg = f"The interaction has been completed with status: {status}"
        
        if summary:
            try:
                workspace_root = Path(os.getcwd()) / "workspace"
                workspace_root.mkdir(parents=True, exist_ok=True)
                summary_path = workspace_root / "session_summary.md"
                with open(summary_path, "w", encoding="utf-8") as f:
                    f.write(summary)
                result_msg += f"\n\n📝 Session summary saved to `session_summary.md`."
            except Exception as e:
                result_msg += f"\n\n⚠️ Failed to save session summary: {e}"

        if follow_up_suggestions:
            result_msg += "\n\n💡 **Suggested Follow-up:**"
            for i, suggestion in enumerate(follow_up_suggestions, 1):
                result_msg += f"\n{i}. {suggestion}"
                
        return result_msg
