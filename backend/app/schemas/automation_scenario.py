from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AutomationScenarioCreate(BaseModel):
    name: str
    description: str
    playbook_path: str

class AutomationScenarioUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    playbook_path: str | None = None
    is_active: bool | None = None

class AutomationScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    playbook_path: str
    is_active: bool
    created_at: datetime