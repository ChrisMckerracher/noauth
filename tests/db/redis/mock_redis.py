from unittest.mock import Mock, MagicMock

from noauth.db.redis.redis_entity import RedisEntity

#We can't mock directly from this for some reason so still need to patch
class MockRedisQuery(MagicMock):
    pass



class MockRedisEntity(RedisEntity, Mock):
    index: str = "mock_index"

    @classmethod
    def query(cls, client: Mock):
        return MockRedisQuery()

    def __eq__(self, other):
        return self.index == other.index and \
            self.id == other.id
