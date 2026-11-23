from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress
from datetime import datetime
from enum import StrEnum

class ServerStatus(StrEnum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    MAINTENANCE = 'MAINTENANCE'

class ServerType(StrEnum):
    WEB = 'WEB'
    DATABASE = 'DATABASE'
    APPLICATION = 'APPLICATION'
    OTHER = 'OTHER'

class ServerEnvironment(StrEnum):
    PRODUCTION = 'PRODUCTION'
    TEST = 'TEST'
    DEVELOPMENT = 'DEVELOPMENT'

class ServerCreate(BaseModel):
    hostname: str = Field(min_length=1, max_length=255)
    ip_address: IPvAnyAddress
    server_type: str = ServerType
    os: str = Field(min_length=1, max_length=100)
    os_version: str | None = Field(default=None, min_length=1, max_length=50)
    environment: ServerEnvironment | None = None
    cpu: int | None = Field(default=None, gt=0)
    ram: int | None = Field(default=None, gt=0)
    description: str | None = None

class ServerUpdate(BaseModel):
    hostname: str | None = Field(default=None, min_length=1, max_length=255)
    ip_address: IPvAnyAddress | None = None
    server_type: ServerType | None = None
    os: str | None = Field(default=None, min_length=1, max_length=100)
    os_version: str | None = Field(default=None, min_length=1, max_length=50)
    environment: ServerEnvironment | None = None
    cpu: int | None = Field(default=None, gt=0)
    ram: int | None = Field(default=None, gt=0)
    description: str | None = None
    status: ServerStatus

class ServerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hostname: str
    ip_address: str
    server_type: ServerType | None
    os: str
    os_version: str | None
    environment: str | None
    cpu: int | None
    ram: int | None
    description: str | None
    status: ServerStatus
    created_at: datetime