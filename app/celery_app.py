import os

from celery import Celery
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("CELERY_DB", "0")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

celery = Celery(
    "webhook_app", broker=REDIS_URL, backend=REDIS_URL, include=["app.webhook.tasks"]
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_max_tasks_per_child=200,
    broker_connection_retry_on_startup=True,
)


def init_celery(app: Flask):
    """Initialize Celery with Flask app context"""
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            """Handle task failure"""
            from app.settings.logger import logger

            logger.error(f"Task {task_id} failed: {exc}")
            super().on_failure(exc, task_id, args, kwargs, einfo)

    celery.Task = ContextTask
    return celery
