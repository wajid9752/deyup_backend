from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    
    path("login/" , user_login ),
    path("profile/" , user_profile ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
