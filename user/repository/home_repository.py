from user.models import Home


class HomeRepository:

    @staticmethod
    def get_home_by_user(user) -> Home:
        return user.home.first()
