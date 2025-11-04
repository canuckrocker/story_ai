from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.database import RawInput, User, MemoryBranch
from app.schemas.schemas import RawInputCreate, RawInputResponse

router = APIRouter()


@router.post("/", response_model=RawInputResponse)
def create_raw_input(input_data: RawInputCreate, db: Session = Depends(get_db)):
    """Create a new raw input (text or voice transcription)"""
    # Verify user exists
    user = db.query(User).filter(User.id == input_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify memory branch exists if provided
    if input_data.memory_branch_id:
        branch = db.query(MemoryBranch).filter(
            MemoryBranch.id == input_data.memory_branch_id
        ).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Memory branch not found")

    db_input = RawInput(**input_data.model_dump())
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input


@router.get("/{input_id}", response_model=RawInputResponse)
def get_raw_input(input_id: int, db: Session = Depends(get_db)):
    """Get a specific raw input"""
    raw_input = db.query(RawInput).filter(RawInput.id == input_id).first()
    if not raw_input:
        raise HTTPException(status_code=404, detail="Input not found")
    return raw_input


@router.get("/user/{user_id}", response_model=List[RawInputResponse])
def list_user_inputs(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all inputs for a user"""
    inputs = db.query(RawInput).filter(
        RawInput.user_id == user_id
    ).order_by(RawInput.created_at.desc()).offset(skip).limit(limit).all()
    return inputs


@router.get("/branch/{branch_id}", response_model=List[RawInputResponse])
def list_branch_inputs(branch_id: int, db: Session = Depends(get_db)):
    """List all inputs for a specific memory branch"""
    inputs = db.query(RawInput).filter(
        RawInput.memory_branch_id == branch_id
    ).order_by(RawInput.created_at.desc()).all()
    return inputs


@router.delete("/{input_id}")
def delete_raw_input(input_id: int, db: Session = Depends(get_db)):
    """Delete a raw input"""
    raw_input = db.query(RawInput).filter(RawInput.id == input_id).first()
    if not raw_input:
        raise HTTPException(status_code=404, detail="Input not found")

    db.delete(raw_input)
    db.commit()
    return {"message": "Input deleted successfully"}
