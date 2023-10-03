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
from .serializers import ProfileSerializer
# Create your views here.

# Profile :
# # subscription 
def token_api(email):
    url = 'http://65.0.183.157/token/'
    payload =  {
            'email': email, 
            'password': email, 
           }    
    r = requests.post(url=url, data=payload)
    response=json.loads(r.text)
    print(response)
    token=response['access']
    return token



@api_view(['POST'])
def user_login(request):
    try:
        get_data = json.loads(request.body)
        getEmail = get_data['email']
        if User.objects.filter(email=getEmail).exists():
            print(User.objects.filter(email=getEmail).first().email)
        else:
            Obj=User.objects.create(email=getEmail)
            Obj.set_password(getEmail)
            Obj.save()
        
        getToken=token_api(getEmail)
        
        data={
            "status":status.HTTP_200_OK,
            'message':'Otp sent successfully',
            'token': getToken

        }
        return JsonResponse(data)
    except Exception as e:
        data={
            "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message':f'Internal Server Error {e}',
            'token': ''

        }
        return JsonResponse(data)
    




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) 
def user_profile(request):
    obj=User.objects.get(email=request.user.email)
    serializer=ProfileSerializer(obj , many=False)
    data={
            "status":status.HTTP_200_OK,
            'message':'Profile Fetched Successfully' ,
            'data':{
                'user': serializer.data ,
            }
        }
    return JsonResponse(data)

    
    
