import importlib
import pkgutil
from pathlib import Path
from django.apps import AppConfig


class HardwareConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hardware"

    def ready(self):
        from . import __path__ as hardware_path

        for _, module_name, is_pkg in pkgutil.iter_modules(hardware_path):
            if is_pkg and Path(f"{hardware_path[0]}/{module_name}/device.py").is_file():
                importlib.import_module(f"hardware.{module_name}.device")
