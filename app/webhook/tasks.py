from datetime import datetime
from datetime import timezone

from app.celery_app import celery
from app.celery_mongo import celery_mongo
from app.celery_mongo import init_celery_mongo
from app.settings.logger import logger

init_celery_mongo()


@celery.task(bind=True)
def async_store_event(self, data):
    try:
        data["timestamp"] = datetime.now(timezone.utc).strftime(
            "%d %B %Y - %I:%M:%S %p UTC"
        )
        if celery_mongo.db is None:
            logger.error("MongoDB connection not initialized in Celery task")
            raise Exception("Database connection not available")

        celery_mongo.db.github_webhooks.insert_one(data)
        return {"status": "stored", "task_id": self.request.id}
    except Exception as e:
        logger.error(f"Error in async_store_event: {str(e)}")
        raise
