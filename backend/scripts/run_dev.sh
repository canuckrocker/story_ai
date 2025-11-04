#!/bin/bash

# Story AI - Development Server Startup Script

echo "🚀 Starting Story AI Development Server"
echo "======================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "Please edit .env with your API keys before continuing."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if database is running
echo "🔍 Checking database connection..."
if ! nc -z localhost 5432 2>/dev/null; then
    echo "⚠️  PostgreSQL not detected on localhost:5432"
    echo "Please start PostgreSQL or run: docker-compose up -d postgres"
    exit 1
fi

# Initialize database if needed
echo "🗄️  Checking database tables..."
python scripts/init_db.py

# Start the server
echo ""
echo "✨ Starting FastAPI server..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --port 8000
