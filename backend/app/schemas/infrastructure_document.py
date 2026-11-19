from pydantic import BaseModel, Field

from datetime import datetime

class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    justification: str | None = None

class DocumentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    justification: str | None = None

class DocumentResponse(BaseModel):
    id: int
    author_id: int
    title: str
    description: str | None
    justification: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None