from django.shortcuts import render

from .models import Message
from .utils import send_results

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def check_api(request):

    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_daily_messages(resquest):

    if resquest.method == 'GET':
        try:
            messages = Message.recover_message()
            sent_results = {}
            for msg in list(messages):
                msg.edit_message(msg)
                sent_results[msg] = msg.send_message(msg)

            print(sent_results)
            send_results(sent_results)

            return Response(status=status.HTTP_200_OK)
        
        except: 
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


