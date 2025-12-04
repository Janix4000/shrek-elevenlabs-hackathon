# Shrek ElevenLabs Hackathon

A basic FastAPI template for the Shrek ElevenLabs Hackathon project.

## Features

- ✨ FastAPI framework with automatic interactive API documentation
- 🚀 Basic endpoints (root and health check)
- 📝 Pydantic models for request/response validation
- 🔧 Easy to extend and customize

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Janix4000/shrek-elevenlabs-hackathon.git
cd shrek-elevenlabs-hackathon
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
# Using uvicorn directly
uvicorn main:app --reload

# Or run the main.py file
python main.py
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Root Endpoint
- **URL**: `/`
- **Method**: GET
- **Description**: Returns a welcome message and available endpoints

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Description**: Verifies the API is running
- **Response**: 
  ```json
  {
    "status": "healthy",
    "message": "API is running successfully"
  }
  ```

## Development

To add new endpoints, edit the `main.py` file and add your route handlers.

Example:
```python
@app.get("/your-endpoint")
async def your_function():
    return {"message": "Your response"}
```

## Project Structure

```
shrek-elevenlabs-hackathon/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Next Steps

This is a basic template. You can extend it with:
- Database integration (SQLAlchemy, MongoDB, etc.)
- Authentication and authorization
- Additional API endpoints
- Background tasks
- WebSocket support
- And more!

## License

[Add your license here]