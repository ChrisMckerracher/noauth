from noauth.iam.user.model.user import User
from noauth.iam.user.model.user_role import UserRole


class Admin(User):
    role = UserRole.ADMIN
