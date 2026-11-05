from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime

class InfrastructureDocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    justification: str | None = None

class InfrastructureDocumentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    justification: str | None = None

class InfrastructureDocumentResponse(BaseModel):
    id: int
    author_id: int
    title: str
    description: str | None
    justification: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None