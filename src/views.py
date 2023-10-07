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
from .models import *
from .serializers import ProfileSerializer , stripPlanSerializer
import jwt
import stripe
import time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
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
    return response



@api_view(['POST'])
def user_login(request):
    try:
        getReq=request.META

        getClient=request.headers.get('clientid')
        getPlatform=request.headers.get('platform')
        getTimezone=request.headers.get('timezone')
        
        if not Security_Model.objects.filter(client_id=getClient).exists():
                context= {
                "data": {
                    "token": ""
                    }
                    }
                return JsonResponse(context , status=status.HTTP_401_UNAUTHORIZED)
        
        get_data = json.loads(request.body)
        getToken = get_data['access_token']
        decoded_token = jwt.decode(getToken, options={"verify_signature": False})
        getEmail = decoded_token['email']
        getName =   decoded_token['name']
        if User.objects.filter(email=getEmail).exists():
            getEmail = User.objects.filter(email=getEmail).first().email
            print(getEmail)
        else:
            Obj=User.objects.create(email=getEmail , username=getName , fcm_token=str(getToken))
            Obj.set_password(getEmail)
            Obj.save()
        
        getToken=token_api(getEmail)
        
        context= {
                "data": {
                    "token": getToken['access'] ,
                    "refresh": getToken['refresh']
                    }
                    }
        return JsonResponse(context , status=status.HTTP_200_OK)
        
    except Exception as e:
        context= {
                
                "data": {
                    "token": ""
                    }
                    }
        return JsonResponse(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])      
def  logout_view(request):
    try:
        getdata =  json.loads(request.body)
        token = RefreshToken(getdata["refresh_token"])
        token.blacklist()
        context={
              "bacl":"listed"
        }
        return JsonResponse(context ,status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        print("This is my error : ",e)
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) 
def user_profile(request):
    getClient=request.headers.get('clientid')
    getPlatform=request.headers.get('platform')
    getTimezone=request.headers.get('timezone')
    
    if not Security_Model.objects.filter(client_id=getClient).exists():
            data={
            'data':{
                    'user': "",
                }
            }
            return JsonResponse(data , status=status.HTTP_401_UNAUTHORIZED)

    obj=User.objects.get(email=request.user.email)
    serializer=ProfileSerializer(obj , many=False)
    data={
            'data':{
                'user': serializer.data ,
            }
        }
    return JsonResponse(data , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) 
def plans_api(request):
    getClient=request.headers.get('clientid')
    getPlatform=request.headers.get('platform')
    getTimezone=request.headers.get('timezone')
    
    if not Security_Model.objects.filter(client_id=getClient).exists():
            data={
            'data':{
                    'plans': "",
                }
            }
            return JsonResponse(data , status=status.HTTP_401_UNAUTHORIZED)

    objs=Strip_Plan.objects.filter(status=True)
    serializer=stripPlanSerializer(objs , many=True)
    data={
            'data':{
                'plans': serializer.data ,
            }
        }
    return JsonResponse(data , status=status.HTTP_200_OK)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_payment(request):
    try:
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
            
        checkout_session = stripe.checkout.Session.create(
                customer_email =    request.user.email,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
        return JsonResponse({'payment_link': checkout_session['url'] } , status=status.HTTP_201_CREATED)
    except Exception as e:
          print("Error is ",e)
          return JsonResponse({'payment_link': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def payment_successful(request):
    print(request)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    print("checkout_session_id is",checkout_session_id)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    print("session",session)
    customer = stripe.Customer.retrieve(session.customer)
    print("customer",customer)
    return HttpResponse("All Good Payment is success")





@csrf_exempt
def stripe_webhook(request):
	stripe.api_key =  settings.STRIPE_SECRET_KEY
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
	return HttpResponse(status=200)


