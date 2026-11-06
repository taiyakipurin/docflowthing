import json
from pathlib import Path
from sqlalchemy import select
from datetime import datetime

from app.core.database import SessionLocal, Base, engine
from app.models.automation_scenario import AutomationScenario
from app.models.role import Role
from app.models.user import User
from app.models.server import Server
from app.models.infrastructure_document import InfrastructureDocument
from app.models.approval_decision import ApprovalDecision

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

            session.commit()

            print('ok')

        except Exception as e:
            session.rollback()

            raise e

if __name__ == '__main__':
    seed()