from app.services.redis_service import (
    store_refresh,
    get_refresh,
    delete_refresh
)

token = 'dadassada'

store_refresh(token, user_id=16, ttl=60)
user_id = get_refresh(token)
print(user_id)

delete_refresh(token)

user_id = get_refresh(token)
print(user_id)


