from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.deps import get_db, get_current_user
from app.models.user import User
from app.models.challenge import Challenge
from app.models.repository import Repository
from app.schemas.challenge import ChallengeCreate, ChallengeResponse

router = APIRouter()

@router.post("/", response_model=ChallengeResponse)
def create_challenge(
    challenge_in: ChallengeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "author"]:
        raise HTTPException(status_code=403, detail="Only Admins and Authors can create challenges.")

    # Verify repository exists in this organization
    repo = db.query(Repository).filter(
        Repository.id == challenge_in.repository_id,
        Repository.organization_id == current_user.organization_id
    ).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")

    new_challenge = Challenge(
        organization_id=current_user.organization_id,
        author_id=current_user.id,
        repository_id=repo.id,
        title=challenge_in.title,
        description=challenge_in.description,
        difficulty=challenge_in.difficulty,
        language=challenge_in.language,
        evaluation_config=challenge_in.evaluation_config
    )
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    return new_challenge

@router.get("/", response_model=List[ChallengeResponse])
def list_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Challenge).filter(Challenge.organization_id == current_user.organization_id).all()