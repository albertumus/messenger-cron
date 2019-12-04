from django.test import TestCase, Client
from django.urls import reverse

from .models import Message, Date

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
    def test_daily_messages(self):
        self.client = APIClient()
        self.response = self.client.get(reverse('send-daily-messages'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

# Functions test
