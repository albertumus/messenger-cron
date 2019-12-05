from django.shortcuts import render

from .models import Message

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def check_api(request):

    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def send_daily_messages(resquest):

    if resquest.method == 'GET':
        try:
            messages = Message.recover_messages()
            
            for msg in list(messages):
                msg.edit_message(msg)
            return Response(status=status.HTTP_200_OK)
        
        except: 
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

