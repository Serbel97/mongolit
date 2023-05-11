from apps.user_role import UserRole


class UserObjectChecker:
    @staticmethod
    def user(request_user: dict, user: dict):
        if request_user['_id'] == user['_id']:
            return True

        if request_user['group'] == UserRole.ADMIN:
            return True

        return False
