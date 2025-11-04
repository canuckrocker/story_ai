from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class StoryBranchType(str, enum.Enum):
    CHILDHOOD = "childhood"
    EDUCATION = "education"
    CAREER = "career"
    FAMILY = "family"
    TRAVEL = "travel"
    HOBBIES = "hobbies"
    RELATIONSHIPS = "relationships"
    LEARNINGS = "learnings"
    ADVENTURES = "adventures"
    SKILLS = "skills"
    LIFE_STORIES = "life_stories"
    TIPS = "tips"
    ACCOMPLISHMENTS = "accomplishments"
    FAILURES = "failures"
    CHALLENGES = "challenges"
    GRATEFUL = "grateful"
    GENERAL = "general"


class InputType(str, enum.Enum):
    VOICE = "voice"
    TEXT = "text"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone_number = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    memory_branches = relationship("MemoryBranch", back_populates="user", cascade="all, delete-orphan")
    raw_inputs = relationship("RawInput", back_populates="user", cascade="all, delete-orphan")
    stories = relationship("Story", back_populates="user", cascade="all, delete-orphan")


class MemoryBranch(Base):
    __tablename__ = "memory_branches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    branch_type = Column(Enum(StoryBranchType), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="memory_branches")
    raw_inputs = relationship("RawInput", back_populates="memory_branch", cascade="all, delete-orphan")
    stories = relationship("Story", back_populates="memory_branch", cascade="all, delete-orphan")


class RawInput(Base):
    __tablename__ = "raw_inputs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    memory_branch_id = Column(Integer, ForeignKey("memory_branches.id"), nullable=True)
    input_type = Column(Enum(InputType), nullable=False)

    # For voice inputs
    telnyx_call_id = Column(String(255), nullable=True)
    audio_url = Column(String(1000), nullable=True)

    # Content
    raw_text = Column(Text, nullable=True)  # Original text or transcription
    transcript_confidence = Column(Integer, nullable=True)  # 0-100 for voice inputs

    # Metadata
    metadata = Column(JSON, nullable=True)  # Additional info like duration, language, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="raw_inputs")
    memory_branch = relationship("MemoryBranch", back_populates="raw_inputs")


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    memory_branch_id = Column(Integer, ForeignKey("memory_branches.id"), nullable=True)

    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)

    # AI-generated metadata
    key_themes = Column(JSON, nullable=True)  # List of themes extracted by AI
    time_period = Column(String(100), nullable=True)  # e.g., "1960s", "childhood"
    people_mentioned = Column(JSON, nullable=True)  # List of people in the story

    # Source tracking
    source_input_ids = Column(JSON, nullable=True)  # IDs of raw_inputs used to generate this story

    # Versioning
    version = Column(Integer, default=1)
    parent_story_id = Column(Integer, ForeignKey("stories.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="stories")
    memory_branch = relationship("MemoryBranch", back_populates="stories")
    parent_story = relationship("Story", remote_side=[id], backref="versions")
