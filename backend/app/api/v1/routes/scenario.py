from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.automation_scenario import (
    AutomationScenarioResponse,
    AutomationScenarioUpdate,
    AutomationScenarioCreate
)
from app.services.scenario_service import (
    get_scenarios as get_scenarios_service,
    get_scenario as get_scenario_service,
    create_scenario as create_scenario_service,
    update_scenario as update_scenario_service
)

router = APIRouter(prefix="/scenario", tags=["Scenarios"])

@router.get('/', response_model=list[AutomationScenarioResponse])
def get_scenarios(db: Session = Depends(get_db)) -> list[AutomationScenarioResponse]:
    return get_scenarios_service(db)

@router.get('/{scenario_id}', response_model=AutomationScenarioResponse)
def get_scenario(
    scenario_id: int,
    db: Session = Depends(get_db)
) -> AutomationScenarioResponse:
    return get_scenario_service(db, scenario_id)

@router.patch('/{scenario_id}', response_model=AutomationScenarioResponse)
def update_scenario(
    scenario_id: int,
    data: AutomationScenarioUpdate,
    db: Session = Depends(get_db)
) -> AutomationScenarioResponse:
    return update_scenario_service(db, scenario_id, data)

@router.post('/', response_model=AutomationScenarioResponse)
def create_scenario(
    data: AutomationScenarioCreate,
    db: Session = Depends(get_db)
) -> AutomationScenarioResponse:
    return create_scenario_service(db, data)