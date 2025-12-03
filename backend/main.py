from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Shrek ElevenLabs Hackathon API",
    description="A basic FastAPI template for the Shrek ElevenLabs Hackathon",
    version="1.0.0"
)


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
        "health": "/health"
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
