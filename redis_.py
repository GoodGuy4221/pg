import redis
from pathlib import Path

redis_client = redis.Redis(host='master.81efb21c-58f7-4723-b7f5-f261fc8a1928.c.dbaas.selcloud.ru',
                           port=6380, db=0, ssl=True, password=r'>?$1[[qv$s>^#lx#x8BL02hB@kwARxS:',
                           ssl_ca_certs=Path('.', 'CA.pem'))

redis_client.set(name='test', value='hgjgfjkgfhk')
print(redis_client.flushall())

redis_client.close()
