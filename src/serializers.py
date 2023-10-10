from rest_framework import serializers
from .models import User , Strip_Plan , Purchase_History


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

class Purchase_HistorySerializer(serializers.ModelSerializer):
    transaction_id = serializers.SerializerMethodField()
    plan_start_date = serializers.SerializerMethodField()
    plan_end_date = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()


    def get_transaction_id(self,obj):
        return obj.transaction_id if obj.transaction_id else ""
    def get_plan_start_date(self,obj):
        return obj.plan_start_date if obj.plan_start_date else ""
    def get_plan_end_date(self,obj):
        return obj.plan_end_date if obj.plan_end_date else ""
    def get_created_at(self,obj):
        return obj.created_at if obj.created_at else ""
    def get_updated_at(self,obj):
        return obj.updated_at if obj.updated_at else ""
    
    class Meta:
        model = Purchase_History
        fields = [
            "plan_id",
            "transaction_id",
            "plan_start_date",
            "plan_end_date",
            "plan_auto_renewal",
            "status",
            "created_at",
            "updated_at"
        ]
