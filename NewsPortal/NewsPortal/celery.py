from celery import Celery
from celery.schedules import crontab

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()

app.conf.beat_schedule = {
    'action_weekly_digest': {
        'task': 'news.tasks.weekly_notify',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
