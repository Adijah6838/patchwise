from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Dict, Any

class ChallengeCreate(BaseModel):
    repository_id: UUID
    title: str
    description: str
    difficulty: str
    language: str
    evaluation_config: Dict[str, Any] = {}

class ChallengeResponse(BaseModel):
    id: UUID
    repository_id: UUID
    title: str
    description: str
    difficulty: str
    language: str
    evaluation_config: Dict[str, Any]
    is_published: str
    created_at: datetime

    class Config:
        from_attributes = True