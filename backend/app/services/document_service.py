from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import InfrastructureDocument, User, ApprovalDecision
from app.schemas.infrastructure_document import DocumentResponse, DocumentCreate, DocumentUpdate
from app.core.exceptions import DocumentNotFoundError, DocumentStateError, DocumentAccessDeniedError

def has_global_document_access(user: User) -> bool:
    user_roles = {role.code for role in user.roles}

    return bool(user_roles & {'ADMIN', 'SYSADMIN', 'AUDITOR'})


def get_documents(
    current_user: User,
    db: Session
) -> list[DocumentResponse]:
    user_roles = {role.code for role in current_user.roles}

    if has_global_document_access(current_user):
        docs = db.scalars(
            select(InfrastructureDocument).order_by(
                InfrastructureDocument.id
            )
        ).all()

    elif 'APPROVER' in user_roles:
        docs = db.scalars(
            select(InfrastructureDocument).where(
                InfrastructureDocument.status == 'submitted'
            ).order_by(InfrastructureDocument.id)
        ).all()
    else:
        docs = db.scalars(
            select(InfrastructureDocument).where(
                InfrastructureDocument.author_id == current_user.id
            ).order_by(InfrastructureDocument.id)
        ).all()

    return [DocumentResponse.model_validate(doc) for doc in docs]

def get_document(db: Session, document_id: int, current_user: User) -> DocumentResponse:
    doc = db.scalar(
        select(InfrastructureDocument).where(
            InfrastructureDocument.id == document_id
        )
    )

    if doc is None:
        raise DocumentNotFoundError

    user_roles = {role.code for role in current_user.roles}

    if has_global_document_access(current_user):
        pass

    elif 'APPROVER' in user_roles:
        if doc.status != 'submitted':
            raise DocumentAccessDeniedError

    elif doc.author_id != current_user.id:
        raise DocumentAccessDeniedError

    return DocumentResponse.model_validate(doc)

def create_document(
    db: Session,
    data: DocumentCreate,
    current_user: User
) -> DocumentResponse:
    doc = InfrastructureDocument(**data.model_dump(), author_id=current_user.id)

    try:
        db.add(doc)
        db.commit()
        db.refresh(doc)
    except Exception:
        db.rollback()
        raise


    return DocumentResponse.model_validate(doc)

def update_document(
    db: Session,
    document_id: int,
    data: DocumentUpdate,
    current_user: User
) -> DocumentResponse:
    doc = db.scalar(
        select(InfrastructureDocument).where(
            InfrastructureDocument.id == document_id
        )
    )

    if doc is None:
        raise DocumentNotFoundError

    if doc.status != 'draft':
        raise DocumentStateError

    if doc.author_id != current_user.id:
        raise DocumentAccessDeniedError

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(doc, key, value)

    try:
        db.commit()
        db.refresh(doc)
    except Exception:
        db.rollback()
        raise

    return DocumentResponse.model_validate(doc)

def approve_document(db: Session, document_id: int, current_user: User) -> DocumentResponse:
    doc = db.scalar(
        select(InfrastructureDocument).where(
            InfrastructureDocument.id == document_id
        )
    )

    if doc is None:
        raise DocumentNotFoundError

    if doc.status != 'submitted':
        raise DocumentStateError

    approval_decision = ApprovalDecision(
        document_id=document_id,
        approver_id=current_user.id,
        decision='approved'
    )

    try:
        doc.status = approval_decision.decision
        db.add(approval_decision)
        db.commit()
        db.refresh(doc)
    except Exception:
        db.rollback()
        raise

    return DocumentResponse.model_validate(doc)

def reject_document(db: Session, document_id: int, current_user: User) -> DocumentResponse:
    doc = db.scalar(
        select(InfrastructureDocument).where(
            InfrastructureDocument.id == document_id
        )
    )

    if doc is None:
        raise DocumentNotFoundError

    if doc.status != 'submitted':
        raise DocumentStateError

    approval_decision = ApprovalDecision(
        document_id=document_id,
        approver_id=current_user.id,
        decision='rejected'
    )

    try:
        doc.status = approval_decision.decision
        db.add(approval_decision)
        db.commit()
        db.refresh(doc)
    except Exception:
        db.rollback()
        raise

    return DocumentResponse.model_validate(doc)

def submit_document(db: Session, document_id: int, current_user: User) -> DocumentResponse:
    doc = db.scalar(
        select(InfrastructureDocument).where(
            InfrastructureDocument.id == document_id
        )
    )

    if doc is None:
        raise DocumentNotFoundError

    if doc.author_id != current_user.id:
        raise DocumentAccessDeniedError

    if doc.status != 'draft':
        raise DocumentStateError

    try:
        doc.status = 'submitted'
        doc.submitted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(doc)
    except Exception:
        db.rollback()
        raise

    return DocumentResponse.model_validate(doc)

#!note: do somethign about auditor (for example, can auditor get drafts etc)