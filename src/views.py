from django.shortcuts import render
from django.http import  JsonResponse , HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework import status
import datetime
import requests
import json
from time import strptime
from .models import User
# Create your views here.

# Profile :
# # subscription 


@api_view(['POST'])
def user_login(request):
    get_data = json.loads(request.body)
    getEmail = get_data['email']
    if User.objects.filter(email=getEmail).exists():
        pass 
    else:
        User.objects.create(email=getEmail)
    
    # send_otp(phone,otp)
    data={
        "status":status.HTTP_200_OK,
        'message':'Otp sent successfully',
        'token': ''

    }
    return JsonResponse(data)

    
