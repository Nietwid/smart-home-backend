import pytest
from django.contrib.auth.models import User
from django.http import Http404
from model_bakery import baker
from user.models import Favourite
from room.models import Room
from device.models import Device
from user.service.favourite_service import FavouriteService


@pytest.mark.django_db
class TestFavouriteService:

    # --- Testy get_user_favourites ---

    def test_get_user_favourites_returns_correct_ids(self, db):
        user = baker.make(User)
        home = baker.make("user.Home")
        home.users.add(user)

        room = baker.make(Room, home=home)
        device = baker.make(Device, home=home)

        fav = baker.make(Favourite, user=user)
        fav.room.add(room)
        fav.device.add(device)

        # Action
        result = FavouriteService.get_user_favourites(user)

        # Assert
        assert room.pk in result["rooms"]
        assert device.pk in result["devices"]
        assert len(result["cameras"]) == 0

    def test_toggle_favourite_adds_item(self, db):
        user = baker.make(User)
        home = baker.make("user.Home")
        home.users.add(user)
        room = baker.make(Room, home=home)

        # Action
        FavouriteService.toggle_favourite(
            user, "room", room.pk, is_already_favourite=False
        )

        # Assert
        assert user.favourite.room.filter(pk=room.pk).exists()

    def test_toggle_favourite_removes_item(self, db):
        user = baker.make(User)
        home = baker.make("user.Home")
        home.users.add(user)
        room = baker.make(Room, home=home)

        fav = baker.make(Favourite, user=user)
        fav.room.add(room)

        # Action
        FavouriteService.toggle_favourite(
            user, "room", room.pk, is_already_favourite=True
        )

        # Assert
        assert not fav.room.filter(pk=room.pk).exists()

    def test_toggle_favourite_security_gate(self, db):
        user_a = baker.make(User)
        home_a = baker.make("user.Home")
        home_a.users.add(user_a)

        home_b = baker.make("user.Home")
        room_b = baker.make(Room, home=home_b)

        # Action & Assert
        with pytest.raises(Http404):
            FavouriteService.toggle_favourite(
                user_a, "room", room_b.pk, is_already_favourite=False
            )

    def test_toggle_favourite_invalid_type_raises_value_error(self, db):
        user = baker.make(User)

        with pytest.raises(ValueError, match="Invalid object type."):
            FavouriteService.toggle_favourite(user, "car", 1, False)
