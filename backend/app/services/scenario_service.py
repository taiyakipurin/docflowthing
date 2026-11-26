from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.automation_scenario import AutomationScenario
from app.schemas.automation_scenario import (
    AutomationScenarioResponse,
    AutomationScenarioCreate,
    AutomationScenarioUpdate
)
from app.core.exceptions import ScenarioNotFoundError

def get_scenario(db: Session, scenario_id: int) -> AutomationScenarioResponse:
    scenario = db.scalar(
        select(AutomationScenario).where(
            AutomationScenario.id == scenario_id
        )
    )

    if scenario is None:
        raise ScenarioNotFoundError

    return AutomationScenarioResponse.model_validate(scenario)

def get_scenarios(db: Session) -> list[AutomationScenarioResponse]:
    scenarios = db.scalars(
        select(AutomationScenario).order_by(AutomationScenario.id)
    ).all()

    return [AutomationScenarioResponse.model_validate(scenario) for scenario in scenarios]

def create_scenario(
    db: Session,
    data: AutomationScenarioCreate
) -> AutomationScenarioResponse:
    scenario = AutomationScenario(**data.model_dump())

    try:
        db.add(scenario)
        db.commit()
        db.refresh(scenario)
    except Exception:
        db.rollback()
        raise

    return AutomationScenarioResponse.model_validate(scenario)

def update_scenario(
    db: Session,
    scenario_id: int,
    data: AutomationScenarioUpdate
) -> AutomationScenarioResponse:
    scenario = db.scalar(
        select(AutomationScenario).where(
            AutomationScenario.id == scenario_id
        )
    )

    if scenario is None:
        raise ScenarioNotFoundError

    update_data = data.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(scenario, key, value)

    try:
        db.commit()
        db.refresh(scenario)
    except Exception:
        db.rollback()
        raise

    return AutomationScenarioResponse.model_validate(scenario)
