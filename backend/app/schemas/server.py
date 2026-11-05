from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ServerCreate(BaseModel):
    hostname: str = Field(min_length=1, max_length=255)
    ip_address: str = Field(min_length=1, max_length=45)
    description: str | None = None

class ServerUpdate(BaseModel):
    hostname: str | None = Field(default=None, min_length=1, max_length=255)
    ip_address: str | None = Field(default=None, min_length=1, max_length=45)
    description: str | None = None
    status: str | None = Field(default=None, max_length=30)

class ServerResponse(BaseModel):
    id: int
    hostname: str
    ip_address: str
    description: str | None
    status: str
    created_at: datetime