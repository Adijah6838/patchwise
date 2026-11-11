from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Dict, Any, Optional

class SubmissionCreate(BaseModel):
    challenge_id: UUID
    code_patch: str

class SubmissionResponse(BaseModel):
    id: UUID
    challenge_id: UUID
    candidate_id: UUID
    status: str
    test_results: Optional[Dict[str, Any]] = None
    execution_logs: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True