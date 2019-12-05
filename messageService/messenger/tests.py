from django.test import TestCase, Client
from django.urls import reverse

from .models import Message, Date, WeekDay

import datetime

from rest_framework.test import APIClient
from rest_framework import status

# Models test
class message_creation(TestCase):
    """  Test Module for Create a Message """
    def test_create_date(self):
        Date.objects.create(date=datetime.date(2019,12,9))
        Date.objects.get(date="2019-12-09").delete()

# Views test
class check_api(TestCase):
    """  Test Module for GET Check API View """
    def test_check_api_view(self):
        self.client = APIClient()
        self.response = self.client.get(reverse('check-api'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

class send_daily_messages(TestCase):
    """ Test Module for Daily Messages Messenger """   

    def setUp(self):
        date_for_test = Date.objects.create(date=datetime.date.today())
        day_for_test = WeekDay.objects.create(day=datetime.date.today().weekday())
        self.message1 = Message.objects.create(name='test_1')        
        self.message2 = Message.objects.create(name='test_2')  
        self.message3 = Message.objects.create(name='test_3')  
        self.message1.date.add(date_for_test)
        self.message1.week_day.add(day_for_test)
        self.message2.week_day.add(day_for_test)
        self.messages = Message.objects.all()

    def test_recover_messages_by_day(self):
        self.messages = Message.recover_message()
        self.assertEqual(len(self.messages), 2)
    
    def test_edit_messages(self):
        self.messages = Message.objects.all()
        for msg in list(self.messages):
            msg.edit_message(msg)

    def test_send_message(self):
        self.messages = Message.objects.all()
        for msg in list(self.messages):
            msg.edit_message(msg)

    def test_daily_messages(self):
        self.client = APIClient()
        self.response = self.client.get(reverse('send-daily-messages'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

