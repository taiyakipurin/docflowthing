from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime

from app.schemas.role import RoleResponse

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=120)
    full_name: str = Field(min_length=1, max_length=255)

class UserUpdate(BaseModel):
    full_name: str = Field(
        default = None,
        min_length=1,
        max_length=100
    )

    is_active: bool | None = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    roles: list[RoleResponse] = Field(default_factory=list)

class UserRolesUpdate(BaseModel):
    roles_ids: list[int] = Field(min_length=1)

    @field_validator('roles_ids')
    @classmethod
    def unique_ids(cls, v):
        if len(v) != len(set(v)):
            raise ValueError('Duplicate ids')

        return v