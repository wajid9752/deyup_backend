from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path("login/" , user_login ),
    path("profile/" , user_profile ),
    path("plans/" , plans_api ),
    path("logout/" , logout_view ),
    path("create-payment/" , create_payment ),
    path("success/" , payment_successful ),
    path("cancel-subscription/" , cancel_subscription ),
    path("subscription-history/" , subscription_history ),
    path("generate-pdf/" , generate_pdf ),
    path("generate_secret/" , generate_secret ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Webhooks 
    path("stripe_webhook/" , stripe_webhook_checkout ),
    path("webhook_recurring/" , webhook_recurring ),
    path("webhook_subscription_canceled/" , webhook_subscription_canceled ),
]
