from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ExecutionActCreate(BaseModel):
    document_id: int
    job_id: int | None = None
    file_path: str

class ExecutionActResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    job_id: int | None
    generated_by: int
    created_at: datetime
    file_path: str