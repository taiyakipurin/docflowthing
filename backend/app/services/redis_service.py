from app.core.security import hash_token
from app.core.redis import redis_client

def store_refresh(token: str, user_id: int, ttl: int) -> None:
    token_hash = hash_token(token)
    key = f'refresh:{token_hash}'

    redis_client.set(
        key,
        str(user_id),
        ex=ttl
    )

def get_refresh(token: str) -> int | None:
    token_hash = hash_token(token)
    key = f'refresh:{token_hash}'

    user_id = redis_client.get(key)

    if user_id is None:
        return None

    return int(user_id)

def delete_refresh(token: str) -> None:
    token_hash = hash_token(token)
    key = f'refresh:{token_hash}'

    redis_client.delete(key)

