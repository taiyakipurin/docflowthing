from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.automation_jobs import AutomationJobCreate, AutomationJobResponse
from app.services.job_service import (
    get_job as get_job_service,
    get_jobs as get_jobs_service,
    create_job as create_job_service
)
from app.core.database import get_db

router = APIRouter(prefix='/automation-job', tags=['Job'])

@router.get('/{job_id}', response_model=AutomationJobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)) -> AutomationJobResponse:
    return get_job_service(job_id, db)

@router.get('/')
def get_jobs(db: Session = Depends(get_db)) -> list[AutomationJobResponse]:
    return get_jobs_service(db)

@router.post('/', response_model=AutomationJobResponse)
def create_job(data: AutomationJobCreate, db: Session = Depends(get_db)) -> AutomationJobResponse:
    return create_job_service(data, db)