from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum

from datetime import datetime

class DocumentStatus(StrEnum):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    justification: str | None = None

class DocumentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    justification: str | None = None

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    title: str
    description: str | None
    justification: str | None
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime | None
    submitted_at: datetime | None
    approved_at: datetime | None
    rejected_at: datetime | None
    author_name: str