from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AutomationJobStatus(StrEnum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class AutomationJobCreate(BaseModel):
    scenario_id: int
    document_id: int

class AutomationJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario_id: int
    document_id: int
    launched_by: int
    status: AutomationJobStatus
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime


