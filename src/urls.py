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
    path("stripe_webhook/" , stripe_webhook ),
    path("cancel-subscription/" , cancel_subscription ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
