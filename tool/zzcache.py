import memcache

cache = memcache.Client(['192.144.41.105:11211'],debug=True)
#件所获取到的数据以键-值对的形式存入memcached中
def set(key,value,timeout=60):
    return cache.set(key,value,timeout)

def get(key):
    return cache.get(key)

def delete(key):
    return cache.delete(key)