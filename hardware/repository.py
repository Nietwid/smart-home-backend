from typing import Any
from django.http import Http404

from hardware.registry import HARDWARE_REGISTRY

class HardwareSchemaRepository:
    @staticmethod
    def get_config_by_name(name:str)-> tuple[Any]:
        if not name in HARDWARE_REGISTRY:
            raise Http404(f"Hardware with name {name} not found")
        return HARDWARE_REGISTRY[name].config_model.model_json_schema(),

    @staticmethod
    def get_configs() -> dict[str, Any]:
        return {
            k:v.config_model.model_json_schema() for k,v in HARDWARE_REGISTRY.items()
        }