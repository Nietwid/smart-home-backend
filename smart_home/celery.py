import os
from celery import Celery, signals

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_home.settings")

app = Celery("smart_home")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


def initialize_ai_on_startup():
    """Load ai models on startup"""
    from ai_assistance.device_model import DeviceModel
    from ai_assistance.intent_model import IntentModel
    from ai_assistance.ai_assistance import AiAssistance

    print("Loading AI models...")
    try:
        intent_model = IntentModel()
        device_model = DeviceModel()
        AiAssistance.initialize(intent_model, device_model)
        print("AI models ready!")
    except Exception as e:
        print(f"ERROR initializing AI: {e}")
        import traceback

        traceback.print_exc()
        raise


@signals.worker_init.connect
def on_worker_init(*args, **kwargs):
    if os.environ.get("CELERY_QUEUE") != "ai":
        return
    print("Worker init signal triggered - initializing AI...")
    initialize_ai_on_startup()
