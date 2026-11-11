from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.deps import get_db, get_current_user
from app.models.user import User
from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate, RepositoryResponse

router = APIRouter()

@router.post("/", response_model=RepositoryResponse)
def create_repository(
    repo_in: RepositoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "author"]:
        raise HTTPException(status_code=403, detail="Only Admins and Authors can register repositories.")

    new_repo = Repository(
        organization_id=current_user.organization_id,
        name=repo_in.name,
        url=repo_in.url,
        language=repo_in.language,
        default_branch=repo_in.default_branch
    )
    db.add(new_repo)
    db.commit()
    db.refresh(new_repo)
    return new_repo

@router.get("/", response_model=List[RepositoryResponse])
def list_repositories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Repository).filter(Repository.organization_id == current_user.organization_id).all()