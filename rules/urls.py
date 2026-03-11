from django.urls import path

from .views import CreateRule

urlpatterns = [path("", CreateRule.as_view(), name="create_rule")]
