from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.models.role import Role
from app.models.user import User

def main():
    Base.metadata.create_all(bind=engine)
    
    with Session(engine) as session:
        role = session.scalar(
            select(Role).where(Role.code == 'INITIATOR')
        )

        if role is None:
            role = Role(
                code='INITIATOR',
                name='Инициатор'
            )

            session.add(role)

        user = session.scalar(
            select(User).where(User.username == 'test_user1')
        )

        if user is None:
            user = User(
                username='test_user1',
                password_hash='qiqiq',
                full_name='John Jefferson'
            )

            session.add(user)
        if role not in user.roles:
            user.roles.append(role)
        
        session.commit()
        
        print(f'User ID: {user.id}')
        print(f'Username: {user.username}')
        print(f'Roles: {[role.code for role in user.roles]}')
        
        result = session.scalar(
            select(User).where(User.username == 'test_user1')
        )
        
        print(f'Retrieved user: {result.full_name}')
        
if __name__ == '__main__':
    main()
    