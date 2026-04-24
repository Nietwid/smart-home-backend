from pydantic import ValidationError

from hardware.base import HardwareValidationError


def validate_pydantic_model(model_cls, data, device, validator_func):
    try:
        instance = model_cls(**data)
        validator_func(instance, device)
    except ValidationError as e:
        return {f".".join(str(x) for x in err["loc"]): err["msg"] for err in e.errors()}
    except HardwareValidationError as e:
        return e.errors
    return {}
