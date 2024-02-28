import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stepik.settings')

app = Celery('Stepik')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое подцепление тасков
app.autodiscover_tasks()


# Ставим таск в повторение каждые две минуты, чтобы было удобнее тестить    
app.conf.beat_schedule = {
    # Имя таска
    'clear-media-folder-every-2-minutes': {
        # Путь до нужной таски
        'task': 'products.tasks.update_is_published',
        # Переодичность
        'schedule': crontab(minute='*/2')
    }
}
