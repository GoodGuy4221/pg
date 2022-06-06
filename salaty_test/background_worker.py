import redis
import sys

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as client:
    while True:
        problem = client.brpop('problems')[1].decode('utf-8')
        print(eval(problem))
