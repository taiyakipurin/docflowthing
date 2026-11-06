from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum

class ApprovalDecisionType(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"

class ApprovalDecisionsCreate(BaseModel):
    document_id: int
    decision: ApprovalDecisionType
    reason: str | None = None

class ApprovalDecisionsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    approver_id: int
    decision: ApprovalDecisionType
    reason: str | None
    decided_at: datetime

