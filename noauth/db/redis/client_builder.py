from redis import Redis
import os

from noauth.zk.zk_cache import ZKCache

zk_cache_host = None
zk_node = None
zk_cache = None

def get_zk_cache_host():
    global zk_cache
    global zk_node
    global zk_cache_host

    mode = None

    if not zk_cache_host:
        zk_cache_host = ZKCache(zk_node=zk_node)

    return zk_cache_host


def get_host():
    global mode
    # PROD or DEV
    mode = os.getenv('MODE', default="DEV")

    if mode == "PROD":
        return get_zk_cache_host().get()
    else:
        return 'localhost'


def get_client() -> Redis:
    # toDO: hardcode now, real stuff lata
    return Redis(host=get_host(), port=6379, decode_responses=True)
