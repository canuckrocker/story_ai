from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.database import Story, User, MemoryBranch
from app.schemas.schemas import (
    StoryCreate,
    StoryResponse,
    StoryUpdate,
    GenerateStoryRequest
)
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/", response_model=StoryResponse)
def create_story(story: StoryCreate, db: Session = Depends(get_db)):
    """Create a new story"""
    # Verify user exists
    user = db.query(User).filter(User.id == story.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify memory branch if provided
    if story.memory_branch_id:
        branch = db.query(MemoryBranch).filter(
            MemoryBranch.id == story.memory_branch_id
        ).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Memory branch not found")

    db_story = Story(**story.model_dump())
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story


@router.get("/{story_id}", response_model=StoryResponse)
def get_story(story_id: int, db: Session = Depends(get_db)):
    """Get a specific story"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.get("/user/{user_id}", response_model=List[StoryResponse])
def list_user_stories(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all stories for a user"""
    stories = db.query(Story).filter(
        Story.user_id == user_id
    ).order_by(Story.created_at.desc()).offset(skip).limit(limit).all()
    return stories


@router.get("/branch/{branch_id}", response_model=List[StoryResponse])
def list_branch_stories(branch_id: int, db: Session = Depends(get_db)):
    """List all stories for a specific memory branch"""
    stories = db.query(Story).filter(
        Story.memory_branch_id == branch_id
    ).order_by(Story.created_at.desc()).all()
    return stories


@router.put("/{story_id}", response_model=StoryResponse)
def update_story(
    story_id: int,
    story_update: StoryUpdate,
    db: Session = Depends(get_db)
):
    """Update a story"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Update fields
    update_data = story_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(story, field, value)

    db.commit()
    db.refresh(story)
    return story


@router.delete("/{story_id}")
def delete_story(story_id: int, db: Session = Depends(get_db)):
    """Delete a story"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    db.delete(story)
    db.commit()
    return {"message": "Story deleted successfully"}


@router.post("/generate", response_model=StoryResponse)
async def generate_story(
    request: GenerateStoryRequest,
    db: Session = Depends(get_db)
):
    """Generate a story from raw inputs using AI"""
    ai_service = AIService(db)
    story = await ai_service.generate_story(
        user_id=request.user_id,
        input_ids=request.input_ids,
        memory_branch_id=request.memory_branch_id,
        style=request.style
    )
    return story
