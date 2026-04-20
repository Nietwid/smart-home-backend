from django.urls import path

from .views import CreateRule, RetrieveUpdateDestroyRule

urlpatterns = [
    path("", CreateRule.as_view(), name="create_rule"),
    path(
        "<int:pk>/",
        RetrieveUpdateDestroyRule.as_view(),
        name="retrieve_update_destroy_rule",
    ),
]
