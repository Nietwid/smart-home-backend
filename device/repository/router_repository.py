from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db.models import QuerySet
from device.models import Router


class RouterRepository:

    @staticmethod
    def get_user_router(user: AbstractBaseUser | AnonymousUser) -> QuerySet[Router]:
        return Router.objects.filter(home__users=user).select_related("home")
