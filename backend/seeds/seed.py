import json
from idlelib.util import fix_win_hidpi
from pathlib import Path
from sqlalchemy import select
from datetime import datetime

from app.core.database import SessionLocal, Base, engine
from app.models import *

SEEDS_DIR = Path(__file__).parent

def load_json(filename: str):
    file_path = SEEDS_DIR / filename

    with file_path.open('r', encoding='UTF-8') as file:
        return json.load(file)

def seed_roles(session):
    roles = load_json('roles.json')

    for role_data in roles:
        existing_role = session.scalar(
            select(Role).where(Role.code == role_data['code'])
        )

        if existing_role is None:
            session.add(Role(**role_data))
        else:
            existing_role.name = role_data['name']

        #ゲンキ？

def seed_users(session):
    users = load_json('users.json')

    roles = session.scalars(select(Role)).all()
    role_map = {role.code: role for role in roles}


    for user_data in users:
        username = user_data['username']

        user_roles = []

        for role_code in user_data['roles']:
            role = role_map.get(role_code)

            if role is None:
                raise ValueError('invalid role', role_code)

            user_roles.append(role)

        existing_user = session.scalar(
            select(User).where(User.username == username)
        )

        if existing_user is None:
            existing_user = User(username=username)

            session.add(existing_user)

        existing_user.full_name = user_data['full_name']
        existing_user.is_active = user_data['is_active']
        existing_user.password_hash = user_data['password_hash']
        existing_user.roles = user_roles

def seed_servers(session):
    servers = load_json('servers.json')

    for server_data in servers:
        existing_server = session.scalar(
            select(Server).where(
                Server.hostname == server_data['hostname']
            )
        )

        if existing_server is None:
            session.add(Server(**server_data))
        else:
            existing_server.ip_address = server_data['ip_address']
            existing_server.description = server_data['description']
            existing_server.status = server_data['status']

def seed_documents(session):
    documents = load_json('infrastructure_documents.json')

    for document_data in documents:
        author = session.scalar(
            select(User).where(
                User.username == document_data['author_username']
            )
        )

        if author is None:
            raise ValueError(f'error: {document_data["author_username"]}')

        submitted_at = document_data['submitted_at']

        if submitted_at is not None:
            submitted_at = datetime.fromisoformat(submitted_at)

        existing_document = session.scalar(
            select(InfrastructureDocument).where(
                InfrastructureDocument.title == document_data['title'],
                InfrastructureDocument.author_id == author.id,
            )
        )

        if existing_document is None:
            existing_document = InfrastructureDocument(
                author_id=author.id,
                title=document_data['title'],
            )

            session.add(existing_document)

        existing_document.description = document_data['description']
        existing_document.justification = document_data['justification']
        existing_document.status = document_data['status']
        existing_document.submitted_at = submitted_at

def seed_approval_decisions(session):
    decisions = load_json('approval_decisions.json')

    for decision_data in decisions:
        document = session.scalar(
            select(InfrastructureDocument).where(
                InfrastructureDocument.title == decision_data['document_title']
            )
        )

        approver = session.scalar(
            select(User).where(
                User.username == decision_data['approver_username']
            )
        )

        if document is None:
            raise ValueError(f'error: {decision_data["document_title"]}')

        if approver is None:
            raise ValueError(f'error: {decision_data["approver_username"]}')

        decided_at = datetime.fromisoformat(decision_data['decided_at'])

        existing_decision = session.scalar(
            select(ApprovalDecision).where(
                ApprovalDecision.document_id == document.id,
                ApprovalDecision.approver_id == approver.id,
            )
        )

        if existing_decision is None:
            existing_decision = ApprovalDecision(
                document_id=document.id,
                approver_id=approver.id
            )

            session.add(existing_decision)

        existing_decision.decision = decision_data['decision']
        existing_decision.reason = decision_data['reason']
        existing_decision.decided_at = decided_at

def seed_automation_scenarios(session):
    automation_scenarios = load_json('automation_scenarios.json')

    for automation_data in automation_scenarios:
        existing_scenario = session.scalar(
            select(AutomationScenario).where(
                AutomationScenario.name == automation_data['name'])
        )

        if existing_scenario is None:
            existing_scenario = AutomationScenario(**automation_data)

            session.add(existing_scenario)
        else:
            existing_scenario.description = automation_data['description']
            existing_scenario.playbook_path = automation_data['playbook_path']
            existing_scenario.is_active = automation_data['is_active']

def seed_automation_jobs(session):
    automation_jobs = load_json('automation_jobs.json')

    for job_data in automation_jobs:
        scenario = session.scalar(
            select(AutomationScenario).where(
                AutomationScenario.name == job_data['scenario_name']
            )
        )

        document = session.scalar(
            select(InfrastructureDocument).where(
                InfrastructureDocument.title == job_data['document_title']
            )
        )

        launcher = session.scalar(
            select(User).where(
                User.username == job_data['launcher_username']
            )
        )

        if scenario is None:
            raise ValueError(f'error: {job_data['scenario_name']}')

        if document is None:
            raise ValueError(f'error: {job_data['document_title']}')

        if launcher is None:
            raise ValueError(f'error: {job_data['launcher_username']}')

        created_at = (
            datetime.fromisoformat(job_data['created_at'])
            if job_data['created_at'] is not None
            else None
        )

        started_at = (
            datetime.fromisoformat(job_data['started_at'])
            if job_data['started_at'] is not None
            else None
        )

        finished_at = (
            datetime.fromisoformat(job_data['finished_at'])
            if job_data['finished_at'] is not None
            else None
        )

        existing_job = session.scalar(
            select(AutomationJob).where(
                AutomationJob.scenario_id == scenario.id,
                AutomationJob.document_id == document.id,
                AutomationJob.created_at >= created_at
            )
        )

        if existing_job is None:
            existing_job = AutomationJob(
                scenario_id=scenario.id,
                document_id=document.id,
                created_at=created_at,
                started_at=started_at,
                finished_at=finished_at,
                launched_by=launcher.id,
                status=job_data['status'],
            )

            session.add(existing_job)

        else:
            existing_job.status = job_data['status']
            existing_job.launched_by = launcher.id
            existing_job.started_at = started_at
            existing_job.finished_at = finished_at

def seed_job_server_results(session):
    job_server_results = load_json('job_server_results.json')

    for result_data in job_server_results:
        scenario = session.scalar(
            select(AutomationScenario).where(
                AutomationScenario.name == result_data['scenario_name']
            )
        )

        document = session.scalar(
            select(InfrastructureDocument).where(
                InfrastructureDocument.title == result_data['document_title']
            )
        )

        server = session.scalar(
            select(Server).where(
                Server.hostname == result_data['server_hostname']
            )
        )

        if scenario is None:
            raise ValueError(f'error: {result_data["scenario_name"]}')

        if document is None:
            raise ValueError(f'error: {result_data["document_title"]}')

        if server is None:
            raise ValueError(f'error: {result_data["server_hostname"]}')

        job_created_at = datetime.fromisoformat(result_data['job_created_at'])

        job = session.scalar(
            select(AutomationJob).where(
                AutomationJob.scenario_id == scenario.id,
                AutomationJob.document_id == document.id,
                AutomationJob.created_at >= job_created_at
            )
        )

        if job is None:
            raise ValueError('job not found')

        started_at = (
            datetime.fromisoformat(result_data['started_at'])
            if result_data['started_at'] is not None
            else None
        )

        finished_at = (
            datetime.fromisoformat(result_data['finished_at'])
            if result_data['finished_at'] is not None
            else None
        )

        existing_result = session.scalar(
            select(JobServerResult).where(
                JobServerResult.job_id == job.id,
                JobServerResult.server_id == server.id,
            )
        )

        if existing_result is None:
            existing_result = JobServerResult(
                job_id=job.id,
                server_id=server.id,
                status=result_data['status'],
                stdout=result_data['stdout'],
                stderr=result_data['stderr'],
                started_at=started_at,
                finished_at=finished_at
            )

            session.add(existing_result)

        else:
            existing_result.status = result_data['status']
            existing_result.stdout = result_data['stdout']
            existing_result.stderr = result_data['stderr']
            existing_result.started_at = started_at
            existing_result.finished_at = finished_at

def seed_execution_acts(session):
    execution_acts = load_json('execution_acts.json')

    for act_data in execution_acts:
        document = session.scalar(
            select(InfrastructureDocument).where(
                InfrastructureDocument.title == act_data['document_title']
            )
        )

        creator = session.scalar(
            select(User).where(User.username == act_data['creator_username'])
        )

        job_created_at = datetime.fromisoformat(act_data['job_created_at'])

        job = session.scalar(
            select(AutomationJob).where(
                AutomationJob.document_id == document.id,
                AutomationJob.created_at == job_created_at
            )
        )

        if document is None:
            raise ValueError(f'error: {act_data['document_id']}')

        if creator is None:
            raise ValueError(f'error: {act_data['creator_username']}')

        if job is None:
            raise ValueError(f'error: {act_data['job_id']}')

        if job.status != 'completed':
            raise ValueError(f'wrong status: {act_data['status']}')

        act = session.scalar(
            select(ExecutionAct).where(
                ExecutionAct.job_id == job.id
            )
        )

        if act is None:
            act = ExecutionAct(
                document_id=document.id,
                job_id=job.id,
                generated_by=creator.id,
                created_at=datetime.fromisoformat(act_data['created_at']),
                file_path=act_data['file_path']
            )

            session.add(act)
        else:
            act.document_id = document.id
            act.generated_by = creator.id
            act.created_at = datetime.fromisoformat(act_data['created_at'])
            act.file_path = act_data['file_path']

def seed_audit_logs(session):
    audit_logs = load_json('audit_logs.json')

    for audit_log_data in audit_logs:
        user = session.scalar(
            select(User).where(User.username == audit_log_data['username'])
        )

        if user is None:
            raise ValueError(f'error: {audit_log_data['username']}')

        entity_id = None

        if audit_log_data['entity_type'] == 'infrastructure_document':
            entity = session.scalar(
                select(InfrastructureDocument).where(
                    InfrastructureDocument.title == audit_log_data['entity_title']
                )
            )

            if entity is None:
                raise ValueError(f'error: {audit_log_data['entity_title']}')

            entity_id = entity.id

        elif audit_log_data['entity_type'] == 'automation_job':
            entity = session.query(AutomationJob).join(
                InfrastructureDocument
            ).filter(
                InfrastructureDocument.title == audit_log_data['entity_title']
            ).order_by(
                AutomationJob.created_at
            ).first()

            if entity is None:
                raise ValueError(f'error: {audit_log_data['entity_title']}')

            entity_id = entity.id

        elif audit_log_data['entity_type'] == 'server':
            entity = session.scalar(
                select(Server).where(
                    Server.hostname == audit_log_data['entity_hostname']
                )
            )

            if entity is None:
                raise ValueError(f'error: {audit_log_data['entity_title']}')

            entity_id = entity.id

        created_at = datetime.fromisoformat(audit_log_data['created_at'])

        existing_log = session.scalar(
            select(AuditLog).where(
                AuditLog.user_id == user.id,
                AuditLog.action == audit_log_data['action'],
                AuditLog.entity_type == audit_log_data['entity_type'],
                AuditLog.entity_id == entity_id,
                AuditLog.created_at == created_at
            )
        )

        if existing_log is None:
            log = AuditLog(
                user_id=user.id,
                action=audit_log_data['action'],
                entity_type=audit_log_data['entity_type'],
                entity_id=entity_id,
                details=audit_log_data['details'],
                created_at=created_at
            )

            session.add(log)

        else:
            existing_log.details = audit_log_data['details']

def seed():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        try:
            seed_roles(session)
            session.flush()

            seed_users(session)
            session.flush()

            seed_servers(session)
            session.flush()

            seed_documents(session)
            session.flush()

            seed_approval_decisions(session)
            session.flush()

            seed_automation_scenarios(session)
            session.flush()

            seed_automation_jobs(session)
            session.flush()

            seed_job_server_results(session)
            session.flush()

            seed_execution_acts(session)
            session.flush()

            seed_audit_logs(session)
            session.flush()

            session.commit()

            print('ok')

        except Exception as e:
            session.rollback()

            raise e

if __name__ == '__main__':
    seed()