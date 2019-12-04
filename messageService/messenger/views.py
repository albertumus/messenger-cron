from django.shortcuts import render

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
        return Response(status=status.HTTP_200_OK)



