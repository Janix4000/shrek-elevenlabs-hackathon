install-backend:
	@echo "📦 Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

# Run backend
run-backend:
	@echo "🚀 Starting FastAPI backend on http://localhost:8000"
	cd backend && source venv/bin/activate && uvicorn main:app --reload

