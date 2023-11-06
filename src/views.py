from django.http import  JsonResponse , HttpResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework import status
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
from datetime import date , datetime , timedelta
from decouple import config
# Create your views here.

stripe.api_key =  config('STRIPE_SECRET_KEY')
class Security:
    @staticmethod
    def security_check(request):
        clientid = request.headers.get('clientid')
        getPlatform = request.headers.get('platform')

        if not Security_Model.objects.filter(client_id=clientid).exists():
            return Security.send_client()
        if not Security_Model.objects.filter(platform=getPlatform).exists():
            return Security.send_platform()
        
        return "ok"
    @staticmethod
    def send_client():
        response = JsonResponse({"data": {}}, status=status.HTTP_400_BAD_REQUEST)
        response['Message'] = "Client id not matched"
        return response

    @staticmethod
    def send_platform():
        response = JsonResponse({"data": {}}, status=status.HTTP_400_BAD_REQUEST)
        response['Message'] = "Provide the Right Platform."
        return response

def handler404(request, *args, **argv):
    return HttpResponse("You are not supposed to be here ")



@api_view(['POST'])
def user_login(request):
    try:
        obj = Security()
        if not obj.security_check(request) == 'ok':
            return obj.security_check(request)
            
        get_data = json.loads(request.body)
        getToken = get_data['access_token']
        # social = get_data['social_type']
        
        decoded_token = jwt.decode(getToken, options={"verify_signature": False})
        getEmail = decoded_token['email']
        getName =   decoded_token['name']
        if User.objects.filter(email=getEmail).exists():
            getEmail = User.objects.filter(email=getEmail).first().email
        else:
            customer = stripe.Customer.create(email=getEmail,name=getName)
            Obj=User.objects.create(email=getEmail , username=getName ,stripe_id=customer['id'] )
            Obj.set_password(getEmail)
            Obj.save()
                    
        user = User.objects.get(email=getEmail)
        if not user.stripe_id:
            customer = stripe.Customer.create(email=user.email,name=user.username)
            user.stripe_id=customer['id']
            user.save()

        refresh = RefreshToken.for_user(user)
        new_time=datetime.now() + timedelta(minutes=20)
        
        context= {
                "data": {
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'token_expiry': new_time.strftime("%Y-%m-%d %H:%M:%S")
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
    obj = Security()
    if not obj.security_check(request) == 'ok':
        return obj.security_check(request)

    obj=User.objects.get(email=request.user.email)
    serializer=ProfileSerializer(obj , many=False)

    hist    = Purchase_History.objects.filter(user_id=obj,payment_status="paid")
    history = Purchase_HistorySerializer(hist , many=True)
    data={'data':{
                'user': serializer.data ,
                'subscription': history.data
            }
        }
    return JsonResponse(data , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) 
def plans_api(request):
    obj = Security()
    if not obj.security_check(request) == 'ok':
        return obj.security_check(request)

    objs=Strip_Plan.objects.filter(status=True)
    serializer=stripPlanSerializer(objs , many=True)
    data={'data':{'plans': serializer.data}}
    return JsonResponse(data , status=status.HTTP_200_OK)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_payment(request):
    try:
        obj = Security()
        if not obj.security_check(request) == 'ok':
            return obj.security_check(request)
        
        getdata =   json.loads(request.body)
        planId =    getdata['plan_id'] 
        getPlan =   Strip_Plan.objects.get(id=planId)
        domain_url = config("DOMAIN_URL")
        #domain_url = 'http://127.0.0.1:8000/'
            
        checkout_session = stripe.checkout.Session.create(
                customer= request.user.stripe_id,
                success_url=domain_url + 'success/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': getPlan.payment_link,
                        'quantity': 1,
                    }
                ]
            )
        Purchase_History.objects.create(
            user_id = request.user , 
            plan_id = getPlan,
            payment_status = checkout_session['payment_status'] ,
            status = False ,
            stripe_id = checkout_session['id']
        )
        
        data={'data':{'payment_link': checkout_session['url']}}
        return JsonResponse(data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        data={'data':{'payment_link': f"{e}",}}
        return JsonResponse(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def payment_successful(request):
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    testing_model.objects.create(payload=str(session),text="payment-session")
    email               = session["customer_details"]["email"]
    stripid             = session["id"]   
    paymentstatus       = session["payment_status"]
    customer            = session["customer"]
    subscription        = session["subscription"]
    invoice_id          = session["invoice"]
    amount_total        = session["amount_total"] // 100
    timestamp = session[ "expires_at"]
    expiry = datetime.utcfromtimestamp(timestamp)
    
    Purchase_History.objects.filter(user_id__email=email ,stripe_id=stripid ).update(
        customer_id         = customer ,
        invoice             = invoice_id ,
        subscripion_id      = subscription ,
        subscription_amount = amount_total,
        payment_status      = paymentstatus,
        plan_start_date     = date.today(),
        plan_end_date       = expiry.date(),
    )
    customer = stripe.Customer.retrieve(session.customer)
    return HttpResponse("All Good Payment is success")

@csrf_exempt
def stripe_webhook_checkout(request):
    WEB_SECRET =  config('WEB_SECRET')
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, WEB_SECRET
        )
        if event['type'] == "checkout.session.completed":
            mydata = event["data"]["object"]
            customer = mydata.get("customer")
            gen_id   = mydata.get("id")
            subscription = mydata.get("subscription")
            
            get_obj=Purchase_History.objects.filter(customer_id=customer ,stripe_id=gen_id).last()
            if get_obj:
                get_obj.status=True 
                get_obj.subscripion_id = subscription
                get_obj.plan_auto_renewal=True 
                get_obj.save()
            
        else:
            print("Unhandled Event")    

    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
    return HttpResponse(status=200)
@csrf_exempt
def webhook_recurring(request):
    WEB_SECRET =  config('WEB_SECRET_Invoice')
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    event = stripe.Webhook.construct_event(
            payload, signature_header, WEB_SECRET
        )
    try:
        if event["type"] ==  "invoice.payment_succeeded":
            mydata = event["data"]["object"]
            customer = mydata.get("customer")
            subscription = mydata.get("subscription")
            expired_at= mydata.get("period_end")
            invoice_id     =  mydata.get("id")
            
            expiry = datetime.utcfromtimestamp(expired_at)
            get_obj=Purchase_History.objects.filter(customer_id=customer , subscripion_id=subscription , status=True).last()
            
            if get_obj:
                Purchase_History.objects.create(
                    user_id = get_obj.user_id ,
                    plan_id = get_obj.plan_id ,
                    customer_id         = get_obj.customer_id ,
                    stripe_id = get_obj.stripe_id ,
                    invoice             = invoice_id ,
                    plan_start_date     = date.today(),
                    plan_end_date       = expiry.date(),
                    plan_auto_renewal   = True ,
                    subscripion_id      = get_obj.subscripion_id ,
                    subscription_amount = get_obj.subscription_amount,
                    payment_status      = "paid",
                    status = True 
                )
        elif event["type"] ==  'invoice.payment_failed':
                testing_model.objects.create(payload=str(event),text="invoice.payment_failed")

    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'invoice.payment_succeeded':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
    return HttpResponse(status=200)        

@csrf_exempt
def webhook_subscription_canceled(request):
    WEB_SECRET =  config('WEB_SECRET_Delete')
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    event = stripe.Webhook.construct_event(
            payload, signature_header, WEB_SECRET
        )
    try:
        if event["type"] == 'customer.subscription.deleted':   
            mydata = event["data"]["object"]
            subscription     = mydata.get("id")
            customer         = mydata.get("customer")
            latest_invoice   = mydata.get("latest_invoice")
            expired_at       = mydata.get("period_end")
            expiry = datetime.utcfromtimestamp(expired_at)

            get_obj=Purchase_History.objects.filter(customer_id=customer , subscripion_id=subscription).last()
            
            if get_obj:
                Purchase_History.objects.create(
                        user_id             = get_obj.user_id ,
                        plan_id             = get_obj.plan_id ,
                        customer_id         = get_obj.customer_id ,
                        stripe_id           = get_obj.stripe_id ,
                        invoice             = latest_invoice ,
                        plan_start_date     = date.today(),
                        plan_end_date       = expiry.date(),
                        plan_auto_renewal   = False ,
                        subscripion_id      = get_obj.subscripion_id ,
                        subscription_amount = get_obj.subscription_amount,
                        payment_status      = "cancelled",
                        status = False 
                    )            
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'customer.subscription.deleted':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
    return HttpResponse(status=200)            

@api_view(['POST'])
def generate_secret(request):
    # subscription = stripe.Subscription.retrieve("sub_1O0KpMSCw8UwFosbGCSzyh3N")
    endpoint = stripe.WebhookEndpoint.create(
    url='https://deyup.in/stripe_webhook/',
    enabled_events=[
        'payment_intent.payment_failed',
        'payment_intent.succeeded',
        'invoice.payment_succeeded',
        'invoice.payment_failed',
        'checkout.session.completed',
        'customer.subscription.deleted'
    ],
    )
    # customers = stripe.Customer.list(email="mawazid1051@gmail.com")
    # subscriptions = stripe.Subscription.list(
    #         customer="cus_OnwiXDsrJXjCjX",
    #         status='all',
    #         expand=['data.default_payment_method']
    # )
    # # single_subscription=stripe.Subscription.get("sub_1O01ZVSCw8UwFosbIDBz9gBK")
    # single_subscription = stripe.Subscription.retrieve("sub_1O01ZVSCw8UwFosbIDBz9gBK")
    return JsonResponse(endpoint)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def cancel_subscription(request):
    try:
        obj = Security()
        if not obj.security_check(request) == 'ok':
            return obj.security_check(request)

        getdata =  json.loads(request.body)
        subId = getdata['subscription'] 
        plan_id = getdata['plan_id'] 
        
        retrieve_sub = stripe.Subscription.retrieve(subId)
        sub_status = retrieve_sub.status
        
        if sub_status == "active": 

            stripe.Subscription.modify(
                subId,
                cancel_at_period_end=True,
                )
            Purchase_History.objects.filter(id=plan_id).update(status=False,
                                                               plan_auto_renewal=False , 
                                                               payment_status="cancelled")
            msg = "Your subscription is canceled Successfully"
        
        elif sub_status == "canceled":
            msg = "Your subscription is alreday canceled"    
        
        data={'data':{} }
    
        response = JsonResponse(data ,status=status.HTTP_200_OK)
        response['Message'] = msg
        return response
    
    except Exception as e:
        print(e)
        response = JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response['Message'] = str(e)
        return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def generate_pdf(request):
    obj = Security()
    if not obj.security_check(request) == 'ok':
        return obj.security_check(request)

    getData = json.loads(request.body)
    getplan_id = getData['plan_id']
    purchase_history = Purchase_History.objects.get(id=getplan_id ,user_id=request.user )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="purchase_history.pdf"'
    p = canvas.Canvas(response)
    p.setStrokeColorRGB(0, 0, 0)  # Set border color to black
    p.rect(50, 580, 500, 260)  # Draw outer rectangle
    p.rect(50, 780, 500,80)  # Draw horizontal line
    p.drawString(100, 820, f"Name:       {purchase_history.user_id.username}")
    p.drawString(100, 800, f"Email:      {purchase_history.user_id.email}")
    p.drawString(100, 740, f"Invoice ID: {purchase_history.invoice}")
    p.drawString(100, 720, f"Plan Title: {purchase_history.plan_id.name}")
    p.drawString(100, 700, f"Start Date: {purchase_history.plan_start_date}")
    p.drawString(100, 680, f"Expiry Date:{purchase_history.plan_end_date}")
    p.drawString(100, 660, f"Plan Description:{purchase_history.plan_id.description}")
    p.drawString(100, 640, f"Subscription Amount:  {purchase_history.subscription_amount}")
    p.rect(50, 580, 500, 40)  # Draw horizontal line for the copyright section
    p.drawString(100, 600, f"Copyright 2022 Probook. All Rights Reserved")
    p.showPage()
    p.save()
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def subscription_history(request):
    try:
        subscriptions=Purchase_History.objects.filter(user_id=request.user).exclude(subscripion_id=None)
        myhistory=Purchase_HistorySerializer(subscriptions , many=True).data
        data={'data':{'subscriptions':myhistory} }
        response = JsonResponse(data ,status=status.HTTP_200_OK)
        response['Message'] = "Subscriptions fetched Successfully"
        return response
    except Exception as e:
        response = JsonResponse({'data':{} } ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response['Message'] = f"{e}"
        return response

