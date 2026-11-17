from app.core.redis import redis_client

redis_client.set('test_key', 'test_value')
value = redis_client.get('test_key')

print(value)

redis_client.delete('test_key')

redis_client.close()