from django.db import models

import datetime 
from xml.dom.minidom import parse, getDOMImplementation
from time import gmtime, strftime

from rest_framework import status
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from messageService.settings import URL_KAPSCH_TOKEN, URL_KAPSCH

class Date(models.Model):
    date = models.DateField(unique=True, blank=False, null=False, verbose_name="Dia programado")

    def __str__(self):
        return str(self.date)

class WeekDay(models.Model):
    day = models.IntegerField(verbose_name="Dia de la semana")

    def __str__(self):
        days = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado' ]
        return str(days[self.day])

class Message(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True, verbose_name="Nombre del fichero")
    date = models.ManyToManyField(Date, blank=True, null=True)
    week_day = models.ManyToManyField(WeekDay, blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def recover_message(cls):     
        return (Message.objects.filter(date__date=datetime.date.today()) | Message.objects.filter(week_day__day=datetime.date.today().weekday())).distinct()

    @classmethod
    def edit_message(cls, name):
        """ String -> None
        OBJ: Edit a message at sets the correct datetime to
        PRE: 
        """
        xml_to_edit = parse('messenger/message_list/{}.xml'.format(name))

        xml_to_edit.getElementsByTagName('publicationTime')[0].firstChild.data = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        start_time = xml_to_edit.getElementsByTagName('overallStartTime')
        data_start_time = start_time[0].firstChild.data.split('T')
        data_start_time[0] = '{}'.format(datetime.date.today())
        start_time[0].firstChild.data = 'T'.join(data_start_time)

        end_time = xml_to_edit.getElementsByTagName('overallEndTime')
        data_end_time = end_time[0].firstChild.data.split('T')
        data_end_time[0] = '{}'.format(datetime.date.today())
        end_time[0].firstChild.data = 'T'.join(data_end_time)
        
        try: 
            start_time[1].firstChild.data = 'T'.join(data_start_time)
            end_time[1].firstChild.data = 'T'.join(data_end_time)
        except:
            None
            
        with open('messenger/message_list/{}.xml'.format(name),'w', encoding='utf-8') as f:
            xml_to_edit.writexml(f, addindent='', newl='', encoding='utf-8') 

    @classmethod
    def send_message(cls, name):
        """ String -> HTTP_Response
        OBJ: Extract the XML Information from the XML File and send it to the API
        PRE: 
        """
        try:
            xmlDataToSend = "{}".format(parse('messenger/message_list/{}.xml'.format(name)).toxml())

            token_key = requests.get(URL_KAPSCH_TOKEN, verify=False).text

            send = requests.post(URL_KAPSCH + '{}'.format(token_key),data=xmlDataToSend, verify=False)
            return send.status_code 

        except: 
            return status.HTTP_400_BAD_REQUEST
        
