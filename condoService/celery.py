import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'condoService.settings')

redis_host = settings.REDIS_HOST

app = Celery('condoService',
             broker=settings.CELERY_BROKER_URL,
             backend=settings.CELERY_BROKER_URL,
             include=['taskEngine.tasks']
             )

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    result_expires=3600,
    timezone='US/Eastern',
    beat_schedule={
        'dataGatheringTask': {
            'task': 'taskEngine.tasks.dataGatheringTask',
            'schedule': crontab(minute=0, hour='*/' + settings.DATA_GATHERING_TASK_FREQUENCY),
        },
    },
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()
