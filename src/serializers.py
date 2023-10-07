from rest_framework import serializers
from .models import User , Strip_Plan


class ProfileSerializer(serializers.ModelSerializer):
    google_id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    apple_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    fcm_token = serializers.SerializerMethodField()
    stripe_id = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        return obj.username if obj.username else ""
    def get_google_id(self , obj):
        return obj.google_id if obj.google_id else ""
    def get_apple_id(self , obj):
        return obj.apple_id if obj.apple_id else ""
    def get_image(self , obj):
        return obj.image.url if obj.image else ""
    def get_fcm_token(self , obj):
        return obj.fcm_token if obj.fcm_token else ""
    def get_stripe_id(self , obj):
        return obj.stripe_id if obj.stripe_id else ""
    
    
    class Meta:
        model   = User
        fields  =  [
            "email" ,
            "username",
            "google_id" ,
            "apple_id" ,
            "image" ,
            "fcm_token" ,
            "stripe_id" 
        ]

class stripPlanSerializer(serializers.ModelSerializer):
    
    image = serializers.SerializerMethodField()

    def get_image(self , obj):
        return obj.image.url if obj.image else ""
    
    class Meta:
        model   = Strip_Plan
        fields  =  [
            "id",
            "name",
            "description",
            "payment_link",
            "image",
            "price",
            "duration",
            "status",
            "created_at",
            "updated_at"
        ]