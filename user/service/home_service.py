from django.db import transaction
from uuid import uuid4
from django.shortcuts import get_object_or_404
from user.models import Home


class HomeService:
    @staticmethod
    def get_user_home(user):
        return get_object_or_404(Home, users=user)

    @classmethod
    @transaction.atomic
    def join_home(cls, user, new_home_uuid):
        new_home = get_object_or_404(Home, add_uid=new_home_uuid)
        old_home = user.home.first()

        if old_home:
            old_home.users.remove(user)
            cls._cleanup_home(old_home)

        new_home.users.add(user)
        new_home.add_uid = uuid4()
        new_home.save()
        return new_home

    @classmethod
    @transaction.atomic
    def leave_and_create_new(cls, user):
        home = cls.get_user_home(user)
        home.users.remove(user)
        cls._cleanup_home(home)

        new_home = Home.objects.create(add_uid=uuid4())
        new_home.users.add(user)
        return new_home

    @staticmethod
    def _cleanup_home(home):
        if home.users.count() == 0:
            home.delete()
