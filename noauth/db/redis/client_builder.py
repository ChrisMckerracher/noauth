from redis import Redis
import os

from noauth.zk_cache.zk_cache import ZKCache

mode = None
zk_cache = None
zk_node = None
zk_cache_host = ZKCache[str](zk_node=zk_node)


def get_host():
    global mode
    # PROD or DEV
    mode = os.environ['MODE']

    if mode is "PROD":
        return zk_cache_host.get()
    else:
        return 'localhost'


def get_client() -> Redis:
    # toDO: hardcode now, real stuff lata
    return Redis(host=get_host(), port=6379, decode_responses=True)
