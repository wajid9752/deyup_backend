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
            "status",
            "created_at",
            "updated_at"
        ]

class Purchase_HistorySerializer(serializers.ModelSerializer):
    invoice = serializers.SerializerMethodField()
    customer_id = serializers.SerializerMethodField()
    stripe_id = serializers.SerializerMethodField()
    subscripion_id = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    subscription_amount = serializers.SerializerMethodField()

    plan_start_date = serializers.SerializerMethodField()
    plan_end_date = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()


    def get_invoice(self,obj):
        return obj.invoice if obj.invoice else ""
    def get_plan_start_date(self,obj):
        return obj.plan_start_date if obj.plan_start_date else ""
    def get_plan_end_date(self,obj):
        return obj.plan_end_date if obj.plan_end_date else ""
    def get_created_at(self,obj):
        return obj.created_at if obj.created_at else ""
    def get_updated_at(self,obj):
        return obj.updated_at if obj.updated_at else ""
    def get_customer_id(self,obj):
        return obj.customer_id if obj.customer_id else ""
    def get_stripe_id(self,obj):
        return obj.stripe_id if obj.stripe_id else ""
    def get_subscripion_id(self,obj):
        return obj.subscripion_id if obj.subscripion_id else ""
    def get_payment_status(self,obj):
        return obj.payment_status if obj.payment_status else ""
    def get_subscription_amount(self,obj):
        return obj.subscription_amount if obj.subscription_amount else ""
    
    class Meta:
        model = Purchase_History
        fields = [
            "id",
            "plan_id",
            "invoice",
            "customer_id",
            "stripe_id",
            "subscripion_id",
            "plan_start_date",
            "plan_end_date",
            "subscription_amount",
            "payment_status",
            "plan_auto_renewal",
            "status",
            "created_at",
            "updated_at"
        ]
