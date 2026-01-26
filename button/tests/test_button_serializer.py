from unittest.mock import patch

import pytest
from rest_framework.serializers import ValidationError
from button.models import ButtonType
from button.serializer import ButtonSerializer, ButtonSerializerDevice


@pytest.mark.django_db
def test_button_serializer_excludes_mac_field(button):
    """
    ButtonSerializer should exclude the 'mac' field
    """
    serializer = ButtonSerializer(button)
    data = serializer.data
    assert "mac" not in data


@pytest.mark.django_db
def test_button_serializer_device_includes_only_button_type(button):
    """
    ButtonSerializerDevice should only include the 'button_type' field
    """
    serializer = ButtonSerializerDevice(button)
    data = serializer.data
    assert list(data.keys()) == ["button_type"]


@pytest.mark.parametrize("button_type", ButtonType.choices)
def test_button_type_should_validate(button_type):
    """
    ButtonSerializer should validate button_type
    """
    serializer = ButtonSerializer(data={"button_type": button_type[0]})
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    assert data["button_type"] == button_type[0]


def test_button_type_should_raise_error():
    """
    ButtonSerializer should raise ValidationError if button_type is invalid
    """
    serializer = ButtonSerializer(data={"button_type": "INVALID"})
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@patch("button.serializer.send_set_settings_request")
@patch("button.serializer.button_type_change")
def test_button_call_button_type_change(
    button_type_change_mock, send_set_settings_request_mock, button
):
    """
    ButtonSerializer should call button_type_change when button_type is changed
    """
    serializer = ButtonSerializer(
        instance=button, data={"button_type": ButtonType.BISTABLE}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    button_type_change_mock.assert_called_once_with(ButtonType.BISTABLE.value, button)
    send_set_settings_request_mock.assert_called_once_with(button)
