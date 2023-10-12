import os
from datetime import datetime, timedelta
from typing import TypeVar, Generic

from kazoo.client import KazooClient
from pydantic import BaseModel

zk_host = os.environ['ZK_HOST']

zk_host = "localhost" if not zk_host else zk_host

T = TypeVar("T", bound=any)


# zookeeper cache
class ZKCache(BaseModel, Generic[T]):
    time: datetime | None = None
    cache_time_seconds: int = 5 * 60
    zk_node: str
    value: T = None

    @classmethod
    def get_client(cls):
        if not cls.zk_client:
            cls.zk_client = KazooClient(hosts=f"{zk_host}:2181")
        return cls.zk_client

    @property
    def client(self):
        return self.get_client()

    def get(self) -> T:
        now = datetime.now()

        if not self.time or now <= self.time + timedelta(seconds=self.cache_time_seconds):
            node = self.client.get(self.zk_node)
            if not node:
                return self.value
            self.time = now
            self.value = node

        return self.value
