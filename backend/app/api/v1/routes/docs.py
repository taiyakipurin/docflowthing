from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.infrastructure_document import DocumentResponse, DocumentCreate, DocumentUpdate
from app.core.database import get_db
from app.models import User
from app.api.dependencies import require_roles, get_current_user
from app.services.document_service import (
    create_document as create_document_service,
    get_documents as get_documents_service,
    get_document as get_document_service,
    update_document as update_document_service,
    submit_document as submit_document_service,
    approve_document as approve_document_service,
    reject_document as reject_document_service
)

router = APIRouter(prefix='/documents', tags=['Documents'])

@router.post('/', response_model=DocumentResponse)
def create_document(
    data: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_document_service(db, data, current_user)

@router.get('/', response_model=list[DocumentResponse])
def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_documents_service(current_user, db)

@router.get('/{document_id}', response_model=DocumentResponse)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    return get_document_service(db, document_id, current_user)

@router.patch('/{document_id}', response_model=DocumentResponse)
def update_document(
    document_id: int,
    data: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_document_service(db, document_id, data, current_user)

@router.post('/{document_id}/submit', response_model=DocumentResponse)
def submit_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return submit_document_service(db, document_id, current_user)

@router.post('/{document_id}/approve', response_model=DocumentResponse)
def approve_document(
    document_id: int,
    current_user: User = Depends(require_roles('APPROVER')),
    db: Session = Depends(get_db)
):
    return approve_document_service(db, document_id, current_user)

@router.post('/{document_id}/reject', response_model=DocumentResponse)
def reject_document(
    document_id: int,
    current_user: User = Depends(require_roles('APPROVER')),
    db: Session = Depends(get_db)
):
    return reject_document_service(db, document_id, current_user)



