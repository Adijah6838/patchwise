import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    difficulty = Column(String, nullable=False) # intermediate, advanced, senior, expert
    language = Column(String, nullable=False)
    
    # Store evaluation rubrics and test configurations as JSON
    evaluation_config = Column(JSON, nullable=False, default={})
    
    is_published = Column(String, default="draft") # draft, published, archived
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)