import os

from celery import Celery

from config.params import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery()
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    '주기적_재고_추가_태스크': {
        'task': 'api.tasks.add_menu_stock_to_all',
        'schedule': STOCK_UPDATE_PERIOD_IN_SEC
    },
    '주기적_포인트_추가_태스크': {
        'task': 'api.tasks.add_user_point_to_all',
        'schedule': POINT_UPDATE_PERIOD_IN_SEC
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
