import logging
import os
from datetime import datetime, timedelta
from typing import TypeVar

from kazoo.client import KazooClient
from pydantic import BaseModel

# ToDo: use this later if we have a need to use cache beyond strings
T = TypeVar("T", bound=any)

logger = logging.Logger(name=__name__, level="DEBUG")


# zookeeper cache
class ZKCache(BaseModel):
    time: datetime | None = None
    cache_time_seconds: int = 5 * 60
    zk_node: str
    value: str | None = None
    zk_host: str = os.getenv('ZK_HOST', default="localhost")

    def get(self) -> str:
        now = datetime.now()

        if not self.time or now >= self.time + timedelta(seconds=self.cache_time_seconds):
            client = KazooClient(hosts=f"{self.zk_host}:2181")
            node = None

            try:
                client.start()
                node = client.get(self.zk_node)
                client.stop()
                if not node:
                    return self.value
            except Exception as e:
                logger.error(f"Unable to connect to ZK: {e}")

            # We can do this more graciously, but for now the 'backoff' of a ZK error is the entire time delta
            # We could do an exponential backoff that increases at max timedelta but it feels overengineered
            self.time = now
            self.value = node

        if self.value:
            return self.value[0].decode('ascii')
        return None
