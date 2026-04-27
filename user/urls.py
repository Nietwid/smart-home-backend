from django.urls import path
from django.urls.resolvers import URLPattern
from .views import (
    LogoutView,
    LoginView,
    RefreshAccessToken,
    RegisterView,
    FavouriteView,
    ChangePasswordView,
    HomeView,
)

urlpatterns: list[URLPattern] = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", RegisterView.as_view(), name="register"),
    path("token/refresh/", RefreshAccessToken.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("favourite/", FavouriteView.as_view(), name="favourite"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("home/", HomeView.as_view(), name="home"),
]
