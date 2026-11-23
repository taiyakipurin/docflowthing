from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.server import ServerResponse, ServerCreate, ServerUpdate
from app.models import Server, User
from app.core.exceptions import ServerNotFoundError, ServerAccessDeniedError

def get_servers(db: Session, user: User) -> list[ServerResponse]:
    servers = db.scalars(
        select(Server) .order_by(Server.id)
    ).all()

    return [ServerResponse.model_validate(server) for server in servers]

def get_server(db: Session, server_id: int, user: User) -> ServerResponse:
    server = db.scalar(
        select(Server).where(Server.id == server_id)
    )

    if server is None:
        raise ServerNotFoundError

    return ServerResponse.model_validate(server)

def create_server(db: Session, data: ServerCreate, user: User) -> ServerResponse:
    server = Server(**data.model_dump())

    try:
        db.add(server)
        db.commit()
        db.refresh(server)
    except Exception:
        db.rollback()
        raise

    return ServerResponse.model_validate(server)

def update_server(db: Session, server_id: int, data: ServerUpdate, user: User) -> ServerResponse:
    server = db.scalar(
        select(Server).where(Server.id == server_id)
    )

    if server is None:
        raise ServerNotFoundError

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(server, key, value)

    try:
        db.add(server)
        db.commit()
        db.refresh(server)
    except Exception:
        db.rollback()
        raise

    return ServerResponse.model_validate(server)

def delete_server(db: Session, server_id: int, user: User) -> ServerResponse:
    server = db.scalar(
        select(Server).where(Server.id == server_id)
    )

    if server is None:
        raise ServerNotFoundError

    response = ServerResponse.model_validate(server)

    try:
        db.delete(server)
        db.commit()
    except Exception:
        raise

    return response



