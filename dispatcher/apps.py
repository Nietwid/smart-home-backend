from django.apps import AppConfig
import pkgutil
import importlib
import logging

logger = logging.getLogger("base")


class DispatcherConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dispatcher"

    def ready(self):
        base_packages = [
            "dispatcher.handlers.cpu.actions",
            "dispatcher.handlers.cpu.events",
            "dispatcher.handlers.peripheral.actions",
            "dispatcher.handlers.peripheral.events",
        ]

        for package_path in base_packages:
            try:
                pkg = importlib.import_module(package_path)
                for loader, module_name, is_pkg in pkgutil.walk_packages(
                    pkg.__path__, pkg.__name__ + "."
                ):
                    importlib.import_module(module_name)
                    logger.info(f"Auto-imported: {module_name}")
            except ModuleNotFoundError as e:
                logger.error(f"ModuleNotFoundError: {e}")
