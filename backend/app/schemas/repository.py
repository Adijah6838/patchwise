from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class RepositoryCreate(BaseModel):
    name: str
    url: str
    language: str
    default_branch: str = "main"

class RepositoryResponse(BaseModel):
    id: UUID
    name: str
    url: str
    language: str
    default_branch: str
    created_at: datetime

    class Config:
        from_attributes = True