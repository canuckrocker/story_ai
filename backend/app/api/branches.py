from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.database import MemoryBranch, User
from app.schemas.schemas import MemoryBranchCreate, MemoryBranchResponse

router = APIRouter()


@router.post("/", response_model=MemoryBranchResponse)
def create_memory_branch(branch: MemoryBranchCreate, db: Session = Depends(get_db)):
    """Create a new memory branch for a user"""
    # Verify user exists
    user = db.query(User).filter(User.id == branch.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_branch = MemoryBranch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


@router.get("/{branch_id}", response_model=MemoryBranchResponse)
def get_memory_branch(branch_id: int, db: Session = Depends(get_db)):
    """Get a specific memory branch"""
    branch = db.query(MemoryBranch).filter(MemoryBranch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Memory branch not found")
    return branch


@router.get("/user/{user_id}", response_model=List[MemoryBranchResponse])
def list_user_branches(user_id: int, db: Session = Depends(get_db)):
    """List all memory branches for a user"""
    branches = db.query(MemoryBranch).filter(MemoryBranch.user_id == user_id).all()
    return branches


@router.delete("/{branch_id}")
def delete_memory_branch(branch_id: int, db: Session = Depends(get_db)):
    """Delete a memory branch"""
    branch = db.query(MemoryBranch).filter(MemoryBranch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Memory branch not found")

    db.delete(branch)
    db.commit()
    return {"message": "Memory branch deleted successfully"}
