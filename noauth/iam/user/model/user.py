from noauth.db.redis.redis_entity import RedisEntity
from noauth.iam.user.model.user_role import UserRole


class User(RedisEntity):
    role: UserRole
    index: str = "user"
