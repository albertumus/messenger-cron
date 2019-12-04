from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messageService.settings')
 
app = Celery('messageService')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls check-api every minute
    sender.add_periodic_task(10.0, check_api.s())

    # Executes send_daily_messages every morning at 06:00 a.m.
    sender.add_periodic_task(
        crontab(hour=6, minute=0),
        sendDailyMessages.s()
    )

@app.task()
def sendDailyMessages():
    r = requests.get('http://localhost:7000/api/check-api')

@app.task()
def check_api():
    r = requests.get('http://localhost:7000/api/check-api')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))