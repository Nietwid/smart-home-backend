from django.shortcuts import get_object_or_404
from camera.models import Camera
from room.models import Room
from device.models import Device
from user.models import Favourite


class FavouriteService:
    MODEL_MAP = {"room": Room, "device": Device, "camera": Camera}

    @classmethod
    def get_user_favourites(cls, user):
        favourite, _ = Favourite.objects.prefetch_related(
            "room", "device", "camera"
        ).get_or_create(user=user)

        return {
            "rooms": list(favourite.room.values_list("id", flat=True)),
            "devices": list(favourite.device.values_list("id", flat=True)),
            "cameras": list(favourite.camera.values_list("id", flat=True)),
        }

    @classmethod
    def toggle_favourite(
        cls, user, obj_type: str, obj_id: int, is_already_favourite: bool
    ):
        model_cls = cls.MODEL_MAP.get(obj_type)
        if not model_cls:
            raise ValueError("Invalid object type.")

        obj = get_object_or_404(model_cls, pk=obj_id, home__users=user)

        favourite, _ = Favourite.objects.get_or_create(user=user)
        m2m_field = getattr(favourite, obj_type)

        if is_already_favourite:
            m2m_field.remove(obj)
        else:
            m2m_field.add(obj)

        return True
