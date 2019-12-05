from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messageService.settings')
 
app = Celery('messageService')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls check-api every minute
    sender.add_periodic_task(60.0, check_api.s())

    # Executes send_daily_messages every morning at 06:00 a.m.
    sender.add_periodic_task(
        crontab(hour=6, minute=0),
        sendDailyMessages.s()
    )

@app.task()
def sendDailyMessages():

    header = {"Content-Type": "application/json"}
    data = json.dumps(
        {
        'username': 'admin',
        'password': 'hola1234'
        }
    )

    request_token = requests.post( settings.SERVICE_URL + "/api/token/" , headers=header, data=data)
    token = json.loads(request_token.content)["access"]

    header_to_r = {'Authorization': 'Bearer {}'.format(token)}
    r = requests.get( settings.SERVICE_URL + '/api/send-daily-messages/', headers=header_to_r)

@app.task()
def check_api():
    r = requests.get(settings.SERVICE_URL + '/api/check-api/')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))