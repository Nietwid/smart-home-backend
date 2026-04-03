from celery import shared_task

@shared_task
def send_microservice_notification(data:dict):
    pass