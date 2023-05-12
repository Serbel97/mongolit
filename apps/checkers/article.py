from apps.user_role import UserRole


class ArticleObjectChecker:
    @staticmethod
    def article(request_user: dict, article: dict):
        if request_user['_id'] == article['author_id']:
            return True

        if request_user['group'] == UserRole.ADMIN.value[0]:
            return True

        return False
