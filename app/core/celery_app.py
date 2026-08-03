from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "moderator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL,
    include=["app.tasks.moderation"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)