from typing import TypeVar, Generic, Optional, get_args

from elasticsearch import Elasticsearch, ApiError
from redis.client import Redis

from noauth.db.es.es_repository import EsRepository
from noauth.db.redis.redis_entity import RedisEntity

import logging

T = TypeVar("T", bound=RedisEntity)
logger = logging.getLogger("EsCacheRepository")


class EsCacheRepository(EsRepository, Generic[T]):
    redis: Redis

    def __init__(self, es: Elasticsearch, redis: Redis, t_cls: T):
        self.t_cls = t_cls
        # ToDo: NO WAY this is the right way to do this...
        index = self.t_cls.model_fields['index'].default
        super().__init__(es, index)
        self.redis = redis

    def save(self, id: str, document: T) -> None:
        # ToDo: write to Redis store and async queue a write to ES task
        self.es.index(index=self.index, id=id, document=document.model_dump_json())

    def get(self, id: str) -> Optional[T]:
        val = self.t_cls.query(client=self.redis).get(id)
        if not val:
            return self.load(id)
        return val

    def load(self, id: str) -> Optional[T]:
        response = None
        try:
            response = self.es.get(index=self.index, id=id)
        except ApiError as e:
            logger.error(f"Experienced error {e} when trying to get id={id} from index={self.index}")

        if not response or not response["found"]:
            return None

        return self.t_cls.model_validate(response["_source"])
