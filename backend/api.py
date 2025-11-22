# Fix for Windows: Use ProactorEventLoop to support subprocess operations
# This MUST be set before any other imports to ensure Playwright works correctly
import sys


if sys.platform == "win32":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import asyncio
import json

from app.agent.manus import Manus
from app.config import config
from app.logger import logger
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


app = FastAPI()

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Capture print/stdout -----
class StdoutInterceptor:
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self._orig_stdout = sys.stdout

    def write(self, data):
        text = data.strip()
        if text:
            try:
                self.queue.put_nowait(text)
            except:
                pass
        self._orig_stdout.write(data)

    def flush(self):
        try:
            self._orig_stdout.flush()
        except:
            pass


@app.websocket("/generate")
async def websocket_generate(ws: WebSocket):
    await ws.accept()

    # Queue for incoming messages from the client
    input_queue: asyncio.Queue[str] = asyncio.Queue()

    # Background task to receive messages
    async def receive_loop():
        try:
            while True:
                data = await ws.receive_text()
                await input_queue.put(data)
        except:
            pass  # Connection closed or error

    receiver_task = asyncio.create_task(receive_loop())

    try:
        # Wait for the initial prompt
        try:
            prompt = await input_queue.get()
            prompt = prompt.strip()
        except:
            return

        if not prompt:
            await ws.send_text("⚠ Empty prompt provided.")
            return

        agent = Manus()

        # Define the callback for user input
        async def ask_user(question: str) -> str:
            # Send the question to the frontend
            # We send a JSON object to distinguish it from normal logs
            logger.info(f"📨 Asking user: {question}")
            msg = json.dumps({"type": "input_request", "content": question})
            await ws.send_text(msg)
            logger.debug(f"📤 Sent input request to frontend")

            # Wait for the user's response
            response = await input_queue.get()
            logger.info(f"📬 Received user response: {response}")

            # Try to parse as JSON if the frontend sends structured data
            try:
                data = json.loads(response)
                if isinstance(data, dict) and data.get("type") == "user_input":
                    logger.debug(f"📝 Parsed structured response")
                    return data.get("content", "")
            except:
                pass

            return response

        # Register the callback
        agent.set_input_callback(ask_user)

        # Async queue for both logs + prints
        log_queue: asyncio.Queue[str] = asyncio.Queue()

        # ---- Intercept Loguru logs ----
        def loguru_sink(message):
            text = message.strip()
            if text:
                try:
                    log_queue.put_nowait(text)
                except:
                    pass

        sink_id = logger.add(loguru_sink, format="{level} - {message}")

        # ---- Intercept print() output ----
        interceptor = StdoutInterceptor(log_queue)
        original_stdout = sys.stdout
        sys.stdout = interceptor  # redirect stdout

        # ---- Task to forward logs + prints to WebSocket ----
        async def forward():
            try:
                while True:
                    msg = await log_queue.get()
                    await ws.send_text(msg)
            except:
                pass

        forward_task = asyncio.create_task(forward())

        # ---- Run the agent ----
        try:
            logger.info("🚀 Starting Manus agent...")
            await agent.run(prompt)  # All prints and logs captured!
            logger.info("🎉 Request finished!")
            await ws.send_text("DONE")

        except Exception as e:
            logger.exception("❌ Manus error occurred.")
            await ws.send_text(f"❌ Error: {e}")

        finally:
            try:
                await agent.cleanup()
            except:
                pass

            # restore stdout
            sys.stdout = original_stdout

            logger.remove(sink_id)
            forward_task.cancel()
            try:
                await forward_task
            except:
                pass

    finally:
        receiver_task.cancel()
        try:
            await receiver_task
        except:
            pass
        await ws.close()


@app.get("/files")
async def list_files():
    """List all files in the workspace directory."""
    files = []
    workspace = config.workspace_root
    if workspace.exists():
        for file in workspace.iterdir():
            if file.is_file() and not file.name.startswith("."):
                files.append(file.name)
    return {"files": sorted(files)}


@app.get("/files/{filename}")
async def get_file(filename: str):
    """Read and return the content of a specific file."""
    file_path = config.workspace_root / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
