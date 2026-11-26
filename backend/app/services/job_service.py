from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import AutomationJob, InfrastructureDocument, AutomationScenario, JobServerResult, Server
from app.schemas.automation_jobs import AutomationJobCreate, AutomationJobResponse
from app.schemas.job_server_result import JobServerResultCreate
from app.core.exceptions import JobNotFoundError, DocumentNotFoundError, ScenarioNotFoundError, ScenarioStateError, \
    DocumentAccessDeniedError, DocumentStateError


def get_job(job_id: int, db: Session):
    job = db.scalar(
        select(AutomationJob).where(
            AutomationJob.id == job_id
        )
    )

    if job is None:
        raise JobNotFoundError

    return job

def get_jobs(db: Session) -> list[AutomationJobResponse]:
    jobs = db.scalars(
        select(AutomationJob).order_by(AutomationJob.id)
    ).all()

    return [AutomationJobResponse.model_validate(job) for job in jobs]

def create_job(data: AutomationJobCreate, db: Session) -> AutomationJobResponse:
    document = db.scalar(
        select(InfrastructureDocument).where(
            InfrastructureDocument.id == data.document_id
        )
    )

    if document is None:
        raise DocumentNotFoundError
    if not document.approved_at:
        raise DocumentStateError

    servers = document.servers

    if not servers:
        raise DocumentStateError #!note: change the exception to DocumentHasNoServersError

    scenario = db.scalar(
        select(AutomationScenario).where(
            AutomationScenario.id == data.scenario_id
        )
    )

    if scenario is None:
        raise ScenarioNotFoundError

    if not scenario.is_active:
        raise ScenarioStateError


    try:
        job = AutomationJob(**data.model_dump())

        db.add(job)
        db.flush()

        for server in servers:
            result = JobServerResult(
                job_id=job.id,
                server_id=server.id,
                status='pending'
            )

            db.add(result)
        db.commit()
        db.refresh(job)
    except Exception:
        db.rollback()
        raise

    return AutomationJobResponse.model_validate(job)
#!note: INTEGRATE ANSIBLE IN THE POST REQUEST
#!note: create job server results notes













