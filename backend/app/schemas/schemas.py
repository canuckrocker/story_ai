from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.database import StoryBranchType, InputType


# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Memory Branch Schemas
class MemoryBranchBase(BaseModel):
    branch_type: StoryBranchType
    title: str
    description: Optional[str] = None


class MemoryBranchCreate(MemoryBranchBase):
    user_id: int


class MemoryBranchResponse(MemoryBranchBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Raw Input Schemas
class RawInputBase(BaseModel):
    input_type: InputType
    raw_text: Optional[str] = None
    memory_branch_id: Optional[int] = None


class RawInputCreate(RawInputBase):
    user_id: int
    telnyx_call_id: Optional[str] = None
    audio_url: Optional[str] = None
    transcript_confidence: Optional[int] = None
    metadata: Optional[dict] = None


class RawInputResponse(RawInputBase):
    id: int
    user_id: int
    telnyx_call_id: Optional[str] = None
    audio_url: Optional[str] = None
    transcript_confidence: Optional[int] = None
    metadata: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Story Schemas
class StoryBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    memory_branch_id: Optional[int] = None


class StoryCreate(StoryBase):
    user_id: int
    key_themes: Optional[List[str]] = None
    time_period: Optional[str] = None
    people_mentioned: Optional[List[str]] = None
    source_input_ids: Optional[List[int]] = None


class StoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    key_themes: Optional[List[str]] = None
    time_period: Optional[str] = None
    people_mentioned: Optional[List[str]] = None


class StoryResponse(StoryBase):
    id: int
    user_id: int
    key_themes: Optional[List[str]] = None
    time_period: Optional[str] = None
    people_mentioned: Optional[List[str]] = None
    source_input_ids: Optional[List[int]] = None
    version: int
    parent_story_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Voice Input Schema (for Telnyx webhook)
class VoiceInputWebhook(BaseModel):
    call_id: str
    from_number: str
    to_number: str
    recording_url: Optional[str] = None
    duration: Optional[int] = None


# AI Generation Schemas
class GenerateStoryRequest(BaseModel):
    user_id: int
    input_ids: List[int]  # IDs of raw inputs to use
    memory_branch_id: Optional[int] = None
    style: Optional[str] = "narrative"  # narrative, bullet_points, timeline, etc.


class SummarizeInputRequest(BaseModel):
    input_id: int
    max_length: Optional[int] = 200
