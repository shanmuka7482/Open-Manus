import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent.manus import Manus
from app.logger import logger

app = FastAPI(title="OpenManus Backend API")

# ✅ Allow frontend & production domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://navaai.vercel.app",  # your deployed frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Early route for Render port detection
@app.get("/")
async def root():
    """
    Simple health route that responds instantly.
    Helps Render detect the open port before Manus finishes loading.
    """
    return {"status": "initializing", "message": "Server is starting up..."}

# ✅ Background Manus initialization
agent = None

@app.on_event("startup")
async def startup_event():
    global agent

    async def initialize_agent():
        global agent
        try:
            logger.info("🧠 Starting Manus initialization in background...")
            agent = await Manus.create()
            logger.info("✅ Manus agent initialized.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Manus: {e}")

    # Don't block startup; run in background
    asyncio.create_task(initialize_agent())

@app.on_event("shutdown")
async def shutdown_event():
    if agent:
        await agent.cleanup()
        logger.info("🧹 Manus agent cleaned up.")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/api/run")
async def run_prompt(request: PromptRequest):
    if not agent:
        return {"error": "Agent not ready yet. Please retry after a few seconds."}
    await agent.run(request.prompt)
    return {"message": "Prompt processed successfully."}

@app.get("/stream")
async def stream_prompt(prompt: str):
    """
    SSE endpoint to stream Manus output to frontend.
    """
    if not agent:
        async def not_ready():
            yield "data: ❌ Agent still starting. Please retry.\n\n"
        return StreamingResponse(not_ready(), media_type="text/event-stream")

    async def event_generator():
        try:
            async for chunk in agent.run_stream(prompt):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: ❌ Error: {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
