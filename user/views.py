import logging
from uuid import uuid4
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django.conf import settings

from user.serializers.change_password_serializer import ChangePasswordSerializer
from user.serializers.custom_token_serializer import CustomTokenObtainPairSerializer
from user.serializers.home_serializer import HomeCodeSerializer
from user.serializers.register_serializer import RegisterSerializer
from user.service.auth_service import AuthService
from user.service.favourite_service import FavouriteService
from user.service.home_service import HomeService
from .models import Favourite, Home

logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
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

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        home = Home.objects.create(add_uid=uuid4())
        home.users.add(user)
        Favourite.objects.create(user=user)

        return Response({"message": "User created successfully"}, status=201)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(
            {"message": "Password updated successfully."}, status=status.HTTP_200_OK
        )


class RefreshAccessToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs) -> Response:
        try:
            access_token = AuthService.refresh_access_token(request)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error refreshing access token: {e}")
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_403_FORBIDDEN,
            )


class LogoutView(APIView):
    def delete(self, request) -> Response:
        try:
            AuthService.logout(request)
            response = Response(status=status.HTTP_204_NO_CONTENT)

            if request.headers.get("X-Client-Type") != "mobile":
                response.delete_cookie("refresh", path="/")

            return response
        except Exception as e:
            logger.error(f"Error logging out: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FavouriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = FavouriteService.get_user_favourites(request.user)
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            FavouriteService.toggle_favourite(
                user=request.user,
                obj_type=request.data.get("type"),
                obj_id=request.data.get("id"),
                is_already_favourite=request.data.get("is_favourite"),
            )
            return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        home = HomeService.get_user_home(request.user)
        return Response({"code": home.add_uid}, status=200)

    def put(self, request, *args, **kwargs):
        serializer = HomeCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        HomeService.join_home(
            user=request.user, new_home_uuid=serializer.validated_data["code"]
        )
        return Response({"message": "Successfully joined new home."}, status=200)

    def delete(self, request, *args, **kwargs):
        HomeService.leave_and_create_new(request.user)
        return Response(status=204)
