from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, inputs, stories, branches, voice
from app.db.config import settings
from app.models.database import Base
from app.db.session import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix=f"/api/{settings.API_VERSION}/users", tags=["users"])
app.include_router(branches.router, prefix=f"/api/{settings.API_VERSION}/branches", tags=["branches"])
app.include_router(inputs.router, prefix=f"/api/{settings.API_VERSION}/inputs", tags=["inputs"])
app.include_router(stories.router, prefix=f"/api/{settings.API_VERSION}/stories", tags=["stories"])
app.include_router(voice.router, prefix=f"/api/{settings.API_VERSION}/voice", tags=["voice"])


@app.get("/")
async def root():
    return {
        "message": "Story AI API",
        "version": settings.API_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
