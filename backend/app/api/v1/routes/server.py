from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import require_roles
from app.models.user import User
from app.schemas.server import ServerCreate, ServerResponse, ServerUpdate
from app.services.server_service import (
    get_servers as get_servers_service,
    get_server as get_server_service,
    create_server as create_server_service,
    delete_server as delete_server_service,
    update_server as update_server_service
)

router = APIRouter(prefix='/servers', tags=['Servers'])

@router.get("/", response_model=list[ServerResponse])
def get_servers(
    current_user: User = Depends(require_roles('SYSADMIN', 'ADMIN')),
    db: Session = Depends(get_db)
):
    return get_servers_service(db, current_user)

@router.get("/{server_id}", response_model=ServerResponse)
def get_server(
    server_id: int,
    current_user: User = Depends(require_roles('SYSADMIN', 'ADMIN')),
    db: Session = Depends(get_db)
):
    return get_server_service(db, server_id, current_user)

@router.post("/", response_model=ServerResponse)
def create_server(
    data: ServerCreate,
    current_user: User = Depends(require_roles('SYSADMIN', 'ADMIN')),
    db: Session = Depends(get_db)
):
    return create_server_service(db, data, current_user)

@router.patch("/{server_id}", response_model=ServerResponse)
def update_server(
    data: ServerUpdate,
    server_id: int,
    current_user: User = Depends(require_roles('SYSADMIN', 'ADMIN')),
    db: Session = Depends(get_db)
):
    return update_server_service(db, server_id, data, current_user)

@router.delete("/{server_id}", response_model=ServerResponse)
def delete_server(
    server_id: int,
    current_user: User = Depends(require_roles('SYSADMIN', 'ADMIN')),
    db: Session = Depends(get_db)
):
    return delete_server_service(db, server_id, current_user)