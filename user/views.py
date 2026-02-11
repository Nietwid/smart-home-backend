from uuid import uuid4, UUID
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser, User
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.views import TokenObtainPairView

from camera.models import Camera
from peripherals.registry import PERIPHERAL_REGISTRY
from peripherals.schemas.light import RGBStripDefinition
from room.models import Room
from device.models import Device
from django.conf import settings
from device.serializers.device import DeviceSerializer
from room.serializer import RoomSerializer
from .models import Favourite, Home
from .serializers import CustomTokenObtainPairSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if request.headers.get("X-Client-Type") != "mobile":
            refresh_token = response.data.get("refresh")
            response.set_cookie(
                key="refresh",
                value=refresh_token,
                samesite="none",
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
                httponly=True,
                secure=True,
            )
        return response


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username: str = request.data.get("username", None)
        password: str = request.data.get("password", None)
        password2: str = request.data.get("password2", None)

        if not username or not password or not password2:
            return Response({"empty": "Proszę uzupełnić pola."}, 400)

        errors = {}
        if User.objects.filter(username=username).exists():
            errors["username"] = "Użytkownik już istnieje."

        if password != password2:
            errors["password2"] = "Hasła nie pasują do siebie."

        home = Home.objects.create()

        if len(errors) > 0:
            return Response(errors, 400)

        user = User.objects.create_user(username=username, password=password)

        home.users.add(user)
        home.add_uid = uuid4()
        home.save()
        Favourite.objects.create(user=user)
        return Response({}, 201)


class ChangePasswordView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        new_password2 = request.data.get("new_password2")
        if not current_password or not new_password or not new_password2:
            return Response({"empty": "Proszę uzupełnić pola."}, 400)

        if not user.check_password(current_password):
            return Response({"current_password": "Błędne hasło."}, 400)

        if new_password != new_password2:
            return Response({"new_password2": "Hasła nie pasują do siebie."}, 400)

        user.set_password(new_password)
        user.save()
        return Response({}, 200)


class RefreshAccessToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs) -> Response:
        try:
            if request.headers.get("X-Client-Type") == "mobile":
                refresh_token_str = request.headers["Token"]
                if not refresh_token_str:
                    return Response({}, status=status.HTTP_403_FORBIDDEN)
            else:
                refresh_token_str: str = request.COOKIES.get("refresh")
                if not refresh_token_str:
                    return Response({}, status=status.HTTP_403_FORBIDDEN)
            refresh_token = RefreshToken(refresh_token_str)
            return Response(
                {"access": str(refresh_token.access_token)}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)


class LogoutView(APIView):
    def delete(self, request) -> Response:
        try:
            if request.headers.get("X-Client-Type", None) == "mobile":
                refresh_token: str = request.headers["Token"]
            else:
                refresh_token: str = request.COOKIES["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            if request.headers["X-Client-Type"] == "mobile":
                return Response({}, status=status.HTTP_200_OK)
            response = Response({}, status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie("refresh", path="/")
            return response
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class FavouriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        favourite, _ = Favourite.objects.prefetch_related(
            "device", "room", "camera"
        ).get_or_create(user=request.user)
        rooms = [room.id for room in favourite.room.all()]
        devices = [device.id for device in favourite.device.all()]
        cameras = [camera.id for camera in favourite.camera.all()]
        return Response(
            {"rooms": rooms, "devices": devices, "cameras": cameras},
            status=status.HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        user = request.user
        action = request.data["is_favourite"]
        if request.data["type"] == "room":
            obj = get_object_or_404(Room, pk=request.data["id"], home__users=user)
            (
                user.favourite.room.remove(obj)
                if action
                else user.favourite.room.add(obj)
            )

        elif request.data["type"] == "device":
            obj = get_object_or_404(Device, pk=request.data["id"])
            (
                user.favourite.device.remove(obj)
                if action
                else user.favourite.device.add(obj)
            )
        elif request.data["type"] == "camera":
            obj = get_object_or_404(Camera, pk=request.data["id"])
            (
                user.favourite.camera.remove(obj)
                if action
                else user.favourite.camera.add(obj)
            )
        else:
            return Response(
                {"error": "Invalid type."}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({}, status=status.HTTP_200_OK)


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        home = get_object_or_404(Home, users=request.user)
        return Response(
            {"code": home.add_uid},
            status=status.HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        code = request.data.get("code")
        if not code:
            return Response(
                {"error": "Code is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            uuid = UUID(code)
        except ValueError:
            return Response(
                {"error": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST
            )
        new_home = get_object_or_404(Home, add_uid=uuid)
        old_home = request.user.home.all().first()
        old_home.users.remove(request.user)

        new_home.users.add(request.user)
        new_home.add_uid = uuid4()
        new_home.save()

        if old_home.users.count() == 0:
            old_home.delete()
        else:
            old_home.save()
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        home = get_object_or_404(Home, users=request.user)
        home.users.remove(request.user)
        if home.users.count() == 0:
            home.delete()
        else:
            home.save()
        new_home = Home.objects.create()
        new_home.users.add(request.user)
        new_home.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
