import hashlib, jwt, secrets, bcrypt
from datetime import datetime, timedelta, timezone

from app.core.config import settings

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(user_id: int, username: str) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        'sub': str(user_id),
        'username': username,
        'iat': now,
        'exp': now + timedelta(minutes=15)
    }

    return jwt.encode(payload, settings.secret_key, algorithm='HS256')

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=['HS256'])

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()

def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)