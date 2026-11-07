from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum

class JobServerResultStatus(StrEnum):
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'
    UNREACHABLE = 'unreachable'

class JobServerResultCreate(BaseModel):
    job_id: int
    server_id: int

class JobServerResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: int
    server_id: int
    status: JobServerResultStatus
    stdout: str | None
    stderr: str | None
    started_at: datetime | None
    finished_at: datetime | None

