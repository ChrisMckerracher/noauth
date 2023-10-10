from elasticsearch import Elasticsearch
from redis.client import Redis

from noauth.db.es.es_cache_repository import EsCacheRepository
from noauth.iam.user.model.user import User

es = Elasticsearch(hosts="http://0.0.0.0:9200")


class UserRepository(EsCacheRepository[User]):

    def __init__(self, es: Elasticsearch, redis: Redis):
        super().__init__(es, redis)

