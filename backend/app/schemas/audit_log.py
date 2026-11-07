from pydantic import BaseModel, ConfigDict
from typing import Any
from datetime import datetime

class AuditLogCreate(BaseModel):
    action: str
    entity_type: str
    entity_id: int | None = None
    details: dict[str, Any] | None = None

class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    action: str
    entity_type: str
    entity_id: int | None
    details: dict[str, Any] | None
    created_at: datetime

