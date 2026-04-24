import pytest
from uuid import uuid4
from django.contrib.auth.models import User
from model_bakery import baker
from user.models import Home
from django.http import Http404
from user.service.home_service import HomeService


@pytest.mark.django_db
class TestHomeService:

    def test_join_home_success(self):
        # Given
        user = baker.make(User)
        old_home = baker.make(Home)
        old_home.users.add(user)

        new_home_uid = uuid4()
        new_home = baker.make(Home, add_uid=new_home_uid)

        # When
        HomeService.join_home(user, new_home_uid)

        # Then
        assert user.home.count() == 1
        assert user.home.first() == new_home
        assert old_home.users.count() == 0

    def test_join_home_regenerates_uid(self):
        # Given
        user = baker.make(User)
        original_uid = uuid4()
        home = baker.make(Home, add_uid=original_uid)

        # When
        HomeService.join_home(user, original_uid)
        home.refresh_from_db()

        # Then
        assert home.add_uid != original_uid
        assert isinstance(home.add_uid, type(uuid4()))

    def test_leave_and_create_new_logic(self):
        # Given
        user = baker.make(User)
        old_home = baker.make(Home)
        old_home.users.add(user)

        # When
        new_home = HomeService.leave_and_create_new(user)

        # Then
        assert user.home.first() == new_home
        assert not Home.objects.filter(id=old_home.pk).exists()
        assert new_home.users.filter(id=user.pk).exists()

    def test_cleanup_home_deletes_empty_house(self):
        # Given
        home = baker.make(Home)

        # When
        HomeService._cleanup_home(home)

        # Then
        assert not Home.objects.filter(id=home.pk).exists()

    def test_cleanup_home_keeps_house_with_users(self):
        # Given
        user = baker.make(User)
        home = baker.make(Home)
        home.users.add(user)

        # When
        HomeService._cleanup_home(home)

        # Then
        assert Home.objects.filter(id=home.pk).exists()

    def test_get_user_home_raises_404_if_no_home(self):
        # Given
        user = baker.make(User)

        # When/Then
        with pytest.raises(Http404):
            HomeService.get_user_home(user)
