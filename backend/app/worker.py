from celery import Celery
from .settings import get_settings

settings = get_settings()
celery_app = Celery('omni_rag', broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(task_serializer='json', accept_content=['json'], result_serializer='json', timezone='UTC', enable_utc=True)

@celery_app.task
def health_task() -> str:
    return 'ok'
