# Story AI - Quick Start Guide

Get your hackathon project running in 5 minutes!

## 🚀 Quick Setup

### Option 1: Using Docker (Recommended)

```bash
# Start everything with Docker
cd story_ai
docker-compose up -d

# API is now running at http://localhost:8000
# Visit http://localhost:8000/docs for interactive API docs
```

### Option 2: Local Development

```bash
cd story_ai/backend

# Run the setup script
./scripts/run_dev.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn app.main:app --reload
```

## 🔑 Required API Keys

Before running, add these to your `.env` file:

1. **PostgreSQL** (local or Docker)
   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/story_ai
   ```

2. **Telnyx** (for voice)
   - Sign up at https://telnyx.com
   - Get API key from dashboard
   ```
   TELNYX_API_KEY=your_key_here
   ```

3. **OpenAI** (for AI story generation)
   - Get from https://platform.openai.com
   ```
   OPENAI_API_KEY=sk-...
   ```

4. **Comet ML** (optional, for tracking)
   - Sign up at https://comet.com
   ```
   COMET_API_KEY=your_key
   COMET_WORKSPACE=your_workspace
   ```

## 🎯 Test Your Setup

```bash
# Check if API is running
curl http://localhost:8000/health

# Run API tests
cd backend
./scripts/test_api.sh
```

## 📱 Basic Usage Flow

### 1. Create a User
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grandma Rose",
    "email": "rose@example.com",
    "phone_number": "+1234567890"
  }'
```

### 2. Create a Memory Branch
```bash
curl -X POST http://localhost:8000/api/v1/branches \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "branch_type": "childhood",
    "title": "Growing up in the 1950s"
  }'
```

### 3. Add a Story Input
```bash
curl -X POST http://localhost:8000/api/v1/inputs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "input_type": "text",
    "raw_text": "I remember my first day of school...",
    "memory_branch_id": 1
  }'
```

### 4. Generate AI Story
```bash
curl -X POST http://localhost:8000/api/v1/stories/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "input_ids": [1],
    "memory_branch_id": 1,
    "style": "narrative"
  }'
```

## 🎨 Frontend Integration

The API is ready for a frontend! Just point your React/Vue/etc app to:
- Base URL: `http://localhost:8000/api/v1`
- WebSocket support: Available for real-time updates
- CORS: Enabled for development

## 🐛 Troubleshooting

**Database connection error?**
```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres
```

**Import errors?**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**API not responding?**
```bash
# Check if port 8000 is available
lsof -i :8000
```

## 📚 Next Steps

1. Check out the interactive docs: http://localhost:8000/docs
2. Read the full README.md
3. Customize memory branch types
4. Add your frontend
5. Set up Telnyx webhooks for voice
6. Deploy to production!

## 🎉 Hackathon Tips

- Start with text inputs before voice
- Use the interactive docs for quick testing
- Comet ML tracking is optional but cool for demos
- Generate multiple story styles to show off AI
- Use the branch system to organize by themes

Good luck with your hackathon! 🚀
