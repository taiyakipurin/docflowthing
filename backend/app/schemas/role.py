from pydantic import BaseModel, ConfigDict

class RoleCreate(BaseModel):
    code: str
    name: str

class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str