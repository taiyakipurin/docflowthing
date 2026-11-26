from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum

class JobServerResultStatus(StrEnum):
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'
    UNREACHABLE = 'unreachable'

class JobServerResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: int
    server_id: int
    status: JobServerResultStatus
    stdout: str | None = None
    stderr: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None

