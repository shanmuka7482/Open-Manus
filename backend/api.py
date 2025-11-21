import sys
import asyncio
from fastapi import FastAPI, WebSocket
from app.agent.manus import Manus
from app.logger import logger   # Loguru logger

app = FastAPI()

# ---- Capture print/stdout -----
class StdoutInterceptor:
    def _init_(self, queue: asyncio.Queue):
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

    try:
        prompt = (await ws.receive_text()).strip()
    except:
        await ws.close()
        return

    if not prompt:
        await ws.send_text("⚠ Empty prompt provided.")
        await ws.close()
        return

    agent = Manus()

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
    sys.stdout = interceptor   # redirect stdout

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
        await agent.run(prompt)     # All prints and logs captured!
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

        await ws.close()
