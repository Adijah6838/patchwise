from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.deps import get_db, get_current_user
from app.models.user import User
from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.workers.tasks import evaluate_submission

router = APIRouter()

@router.post("/", response_model=SubmissionResponse)
def submit_code(
    submission_in: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_sub = Submission(
        challenge_id=submission_in.challenge_id,
        candidate_id=current_user.id,
        code_patch=submission_in.code_patch,
        status="pending"
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    # Trigger the Celery background worker
    evaluate_submission.delay(str(new_sub.id))
    
    return new_sub