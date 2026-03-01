import pytest
from pydantic import ValidationError
from dispatcher.device.messages.payload.basic import (
    DeviceConnectRequest,
)


def test_valid_device_connect_request(mock_device_registry):
    """Ensure valid data passes validation."""
    data = {"wifi_strength": -45, "fun": "lamp", "firmware_version": 1.0}
    req = DeviceConnectRequest(**data)
    assert req.wifi_strength == -45
    assert req.fun == "lamp"


def test_invalid_fun_raises_validation_error(mock_device_registry):
    """Ensure invalid 'fun' raises a ValidationError."""
    data = {"wifi_strength": -60, "fun": "toaster", "firmware_version": 1.0}

    with pytest.raises(ValidationError) as excinfo:
        DeviceConnectRequest(**data)

    assert "Invalid device fun" in str(excinfo.value)


@pytest.mark.parametrize("wifi_strength", [-10, -90, 0])
def test_various_wifi_strength_values(mock_device_registry, wifi_strength):
    """Ensure various wifi_strength values are accepted."""
    req = DeviceConnectRequest(
        wifi_strength=wifi_strength, fun="aquarium", firmware_version=1.0
    )
    assert req.wifi_strength == wifi_strength
