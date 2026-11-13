import hashlib, jwt, secrets, bcrypt
from datetime import datetime, timedelta

from app.core.config import SECRET_KEY

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(user_id: int, username: str) -> str:
    payload = {
        'id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()

def create_refresh_token() -> str:
    token = secrets.token_urlsafe(32)
    # token_hash = hash_token(token)

    return token