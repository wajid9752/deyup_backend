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
from .serializers import ProfileSerializer , stripPlanSerializer,Purchase_HistorySerializer
import jwt
import stripe
import time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from reportlab.pdfgen import canvas
# Create your views here.



def handler404(request, *args, **argv):
    return HttpResponse("You are not supposed to be here ")



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
        # social = get_data['social_type']
        
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
        
        user = User.objects.get(email=getEmail)
        refresh = RefreshToken.for_user(user)
        
        context= {
                "data": {
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    }
                    }
        return JsonResponse(context , status=status.HTTP_200_OK)
        
    except Exception as e:
        context= {"data": {"token": f"{e}"}}
        return JsonResponse(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])      
def  logout_view(request):
    try:
        getdata =  json.loads(request.body)
        token = RefreshToken(getdata["refresh_token"])
        token.blacklist()
        data={"data": {}}
        response = JsonResponse(data ,status=status.HTTP_204_NO_CONTENT)
        response['Message'] = "Logout Successfully"
        return response
    
    except Exception as e:
        data={"data": {}}
        response = JsonResponse(data ,status=status.HTTP_400_BAD_REQUEST)
        response['Message'] = str(e)
        return response


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

    hist    = Purchase_History.objects.filter(user_id=obj)
    history = Purchase_HistorySerializer(hist , many=True)
    data={
            'data':{
                'user': serializer.data ,
                'subscription': history.data
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
        getClient=request.headers.get('clientid')
        if not Security_Model.objects.filter(client_id=getClient).exists():
            data={
            'data':{
                    'payment_link': "",
                }
            }
            return JsonResponse(data , status=status.HTTP_401_UNAUTHORIZED)
        
        
        getdata =  json.loads(request.body)
        planId = getdata['plan_id'] 

        domain_url = 'http://65.0.183.157/'
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
        
        Purchase_History.objects.create(
             user_id = request.user , 
             plan_id = Strip_Plan.objects.get(id=planId),
             status = False
        )
        data={
            'data':{
                    'payment_link': checkout_session['url'],
                }
            }
        return JsonResponse(data, status=status.HTTP_201_CREATED)
    except Exception as e:
          data={
            'data':{
                    'payment_link': f"{e}",
                }
            }
          return JsonResponse(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def cancel_subscription(request):
    getClient=request.headers.get('clientid')
    if not Security_Model.objects.filter(client_id=getClient).exists():
            data={
            'data':{
                    'plans': "",
                }
            }
            return JsonResponse(data , status=status.HTTP_401_UNAUTHORIZED)

    stripe.api_key =  settings.STRIPE_SECRET_KEY
    getdata =  json.loads(request.body)
    subId = getdata['subscription'] 
    plan_id = getdata['plan_id'] 
    
    retrieve_sub = stripe.Subscription.retrieve(subId)
    sub_status = retrieve_sub.status
    print(sub_status)
    if sub_status == "active": 
        mytest=stripe.Subscription.cancel(subId)
        Purchase_History.objects.filter(id=plan_id).update(status=False,plan_auto_renewal=False)
        msg = "Your subscription is canceled Successfully"
    
    elif sub_status == "canceled":
         msg = "Your subscription is alreday canceled"    
    
    data={'data':{} }
  
    response = JsonResponse(data ,status=status.HTTP_200_OK)
    response['Message'] = msg
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def generate_pdf(request):
        
    getData = json.loads(request.body)
    getplan_id = getData['plan_id']

    purchase_history = Purchase_History.objects.get(id=getplan_id)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="purchase_history.pdf"'

    p = canvas.Canvas(response)
    
    # Whole Border Start
    p.setStrokeColorRGB(0, 0, 0)  # Set border color to black
    p.rect(50, 580, 500, 260)  # Draw outer rectangle

    # First Border inside the whole border 
    p.rect(50, 780, 500,80)  # Draw horizontal line
    p.drawString(100, 820, f"Name: {purchase_history.user_id.username}")
    p.drawString(100, 800, f"Email: {purchase_history.user_id.email}")
    # End First Border inside the whole border 

    # Second  Border start inside the whole border 
    # p.rect(50, 600, 500, 140)  # Draw horizontal line
    p.drawString(100, 740, f"Invoice ID: {purchase_history.transaction_id}")
    p.drawString(100, 720, f"Plan Title: {purchase_history.plan_id.name}")
    p.drawString(100, 700, f"Start Date: {purchase_history.plan_start_date}")
    p.drawString(100, 680, f"Expiry Date: {purchase_history.plan_end_date}")
    p.drawString(100, 660, f"Plan Description: {purchase_history.plan_id.description}")
    p.drawString(100, 640, f"Subscription Amount: {purchase_history.subscription_amount}")
    # End Second  Border inside the whole border 
    
    p.rect(50, 580, 500, 40)  # Draw horizontal line for the copyright section
    p.drawString(100, 600, f"Copyright 2022 Probook. All Rights Reserved")
    
    # Whole Border end 

    p.showPage()

    p.save()
    return response
