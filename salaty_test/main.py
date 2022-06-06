import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as client:
    while True:
        problem = input('...')
        client.lpush('problems', problem)
