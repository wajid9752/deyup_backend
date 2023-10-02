from django.db import models

# Create your models here.


class User(models.Model):
    user_name       = models.CharField(max_length=100 , null=True , blank=True)
    email           = models.CharField(max_length=100)
    google_id       = models.CharField(max_length=100 ,null=True , blank=True)
    apple_id        = models.CharField(max_length=100 , null=True , blank=True)
    image           = models.FileField(null=True , blank=True , upload_to="User-Images")
    fcm_token       = models.CharField(max_length=500 , null=True , blank=True)
    stripe_id       = models.CharField(max_length=100 , null=True , blank=True)
    status          = models.BooleanField(default=False)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    # access_token 


class Strip_Plan(models.Model):    
    plan_duration = (
        ('6-Month' , '6-Month'),
        ('1-Year' , '1-Year'),
    )
    name            = models.CharField(max_length=100)
    description     = models.CharField(max_length=100)
    image           = models.FileField(null=True , blank=True , upload_to="Strip-Images")
    price           = models.BigIntegerField()
    duration        = models.CharField(max_length=50 , choices=plan_duration)
    status          = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    


class Purchase_History(models.Model):
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Strip_Plan , on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    plan_start_date = models.DateField()
    plan_end_date = models.DateField()
    plan_auto_renewal = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)





