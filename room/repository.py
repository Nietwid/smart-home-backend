from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from room.models import Room


class RoomRepository:
    @staticmethod
    def get_all_rooms_in_home(user: AbstractBaseUser | AnonymousUser):
        return Room.objects.filter(home__users=user)

    @staticmethod
    def get_all_available_rooms_for_user(user: AbstractBaseUser | AnonymousUser):
        return Room.objects.filter(user=user).union(
            Room.objects.filter(home__users=user).filter(visibility="PU")
        )

    @staticmethod
    def get_room_by_id(room_id: int, user: AbstractBaseUser | AnonymousUser):
        return Room.objects.filter(id=room_id, home__users=user)
