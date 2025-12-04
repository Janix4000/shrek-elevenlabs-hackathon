from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from conversation.controller import router as conversation_router

app = FastAPI(
    title="Shrek ElevenLabs Hackathon API",
    description="API for AI-powered chargeback conversation agent using ElevenLabs",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversation_router)


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {
        "message": "Welcome to Shrek ElevenLabs Hackathon API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "start_conversation": "POST /api/conversation/start",
            "get_conversation_result": "GET /api/conversation/{conversation_id}"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return HealthResponse(
        status="healthy",
        message="API is running successfully"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
