# Story AI - Family Story Preservation Platform

A hackathon project that helps relatives capture and preserve their life stories through voice or text, using AI to organize memories into meaningful narratives for families.

## 🎯 Overview

Story AI allows users to:
- Record stories via voice calls (Telnyx) or text input
- Organize memories into themed branches (childhood, career, adventures, etc.)
- Generate AI-powered narratives from raw memories
- Track and manage different story threads
- Preserve family history for future generations

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Voice**: Telnyx (voice calls & transcription)
- **AI**: OpenAI GPT-4 for story generation
- **ML Tracking**: Comet ML
- **Optimization**: MemVerge for data handling

## 📁 Project Structure

```
story_ai/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   │   ├── users.py
│   │   │   ├── branches.py
│   │   │   ├── inputs.py
│   │   │   ├── stories.py
│   │   │   └── voice.py
│   │   ├── db/           # Database config
│   │   │   ├── config.py
│   │   │   └── session.py
│   │   ├── models/       # SQLAlchemy models
│   │   │   └── database.py
│   │   ├── schemas/      # Pydantic schemas
│   │   │   └── schemas.py
│   │   ├── services/     # Business logic
│   │   │   ├── ai_service.py
│   │   │   ├── telnyx_service.py
│   │   │   └── memverge_service.py
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   └── .env.example
└── docs/
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 14+
- Telnyx account & API key
- OpenAI API key
- Comet ML account (optional)

### Installation

1. **Clone and navigate to project**
```bash
cd story_ai/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL database**
```bash
createdb story_ai
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

6. **Run the application**
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Users
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users/{user_id}` - Get user details
- `GET /api/v1/users/email/{email}` - Get user by email

### Memory Branches
- `POST /api/v1/branches` - Create memory branch
- `GET /api/v1/branches/user/{user_id}` - List user's branches
- `GET /api/v1/branches/{branch_id}` - Get branch details

### Inputs (Voice/Text)
- `POST /api/v1/inputs` - Submit text input
- `GET /api/v1/inputs/user/{user_id}` - List user's inputs
- `GET /api/v1/inputs/branch/{branch_id}` - List branch inputs

### Stories
- `POST /api/v1/stories` - Create story manually
- `POST /api/v1/stories/generate` - Generate story from inputs using AI
- `GET /api/v1/stories/user/{user_id}` - List user's stories
- `PUT /api/v1/stories/{story_id}` - Update story

### Voice (Telnyx)
- `POST /api/v1/voice/webhook` - Telnyx webhook for voice events
- `POST /api/v1/voice/call/initiate` - Initiate outbound call

## 🎭 Memory Branch Types

The system supports organizing stories into these categories:
- **childhood** - Early life memories
- **education** - School and learning experiences
- **career** - Professional life and work
- **family** - Family moments and relationships
- **travel** - Travel adventures
- **hobbies** - Interests and hobbies
- **relationships** - Important relationships
- **learnings** - Life lessons learned
- **adventures** - Exciting experiences
- **skills** - Skills developed
- **life_stories** - General life stories
- **tips** - Advice and tips for family
- **accomplishments** - Achievements and successes
- **failures** - Learning from failures
- **challenges** - Overcoming obstacles
- **grateful** - Things to be grateful for
- **general** - Uncategorized stories

## 🤖 AI Story Generation

The AI service can generate stories in multiple styles:
- **narrative** - Flowing story format (default)
- **bullet_points** - Structured key points
- **timeline** - Chronological timeline
- **letter** - Personal letter to family

Example request:
```json
{
  "user_id": 1,
  "input_ids": [1, 2, 3],
  "memory_branch_id": 5,
  "style": "narrative"
}
```

## 🔊 Telnyx Voice Integration

### Setup
1. Configure webhook URL in Telnyx dashboard: `https://your-domain.com/api/v1/voice/webhook`
2. Add your Telnyx credentials to `.env`
3. Purchase a phone number in Telnyx

### How it works
1. User calls your Telnyx number or you initiate outbound call
2. Call is recorded
3. Recording is transcribed (via Whisper or other service)
4. Transcription is saved as RawInput
5. Multiple inputs can be combined into stories

## 📊 Comet ML Tracking

The system logs to Comet ML:
- Story generation parameters
- AI model performance
- Input/output lengths
- Extracted themes and metadata

## 🗄️ Database Schema

### Users
- User information and authentication

### MemoryBranches
- Organized story categories per user

### RawInputs
- Voice transcriptions and text submissions

### Stories
- Generated narratives with AI-extracted metadata
- Version tracking for story edits

## 🛠️ Development

### Run tests
```bash
pytest tests/
```

### Database migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## 🚀 Deployment

### Using Docker
```bash
docker-compose up -d
```

### Environment variables for production
- Set `DEBUG=False`
- Use production database URL
- Configure CORS allowed origins
- Set up HTTPS/SSL

## 🎯 Hackathon Demo Flow

1. **Create a user**
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Grandma Rose", "email": "rose@example.com", "phone_number": "+1234567890"}'
```

2. **Create memory branches**
```bash
curl -X POST http://localhost:8000/api/v1/branches \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "branch_type": "childhood", "title": "Growing up in the 1950s"}'
```

3. **Submit a story input**
```bash
curl -X POST http://localhost:8000/api/v1/inputs \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "input_type": "text", "raw_text": "I remember when I was 8 years old...", "memory_branch_id": 1}'
```

4. **Generate AI story**
```bash
curl -X POST http://localhost:8000/api/v1/stories/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "input_ids": [1, 2], "memory_branch_id": 1, "style": "narrative"}'
```

## 📝 License

MIT License - feel free to use for your hackathon!

## 🤝 Contributing

Built for hackathon - contributions welcome!

## 📧 Contact

Questions? Reach out during the hackathon!
