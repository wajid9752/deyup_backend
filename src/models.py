from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_active=True, is_admin=False):
        if not email:
            raise ValueError('users must have a email')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            email=email
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username        = models.CharField(max_length=100 , null=True , blank=True)
    email           = models.CharField(max_length=100 , unique=True)
    google_id       = models.CharField(max_length=100 ,null=True , blank=True)
    apple_id        = models.CharField(max_length=100 , null=True , blank=True)
    image           = models.FileField(null=True , blank=True , upload_to="User-Images")
    fcm_token       = models.CharField(max_length=500 , null=True , blank=True)
    stripe_id       = models.CharField(max_length=100 , null=True , blank=True)
    status          = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    objects = UserManager()


    # access_token 
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



class Strip_Plan(models.Model):    
    # plan_duration = (
    #     ('6-Month' , '6-Month'),
    #     ('1-Year' , '1-Year'),
    # )
    name            = models.CharField(max_length=100)
    description     = models.CharField(max_length=100)
    image           = models.FileField(null=True , blank=True , upload_to="Strip-Images")
    payment_link    = models.CharField(max_length=100)
    price           = models.BigIntegerField()
    # duration      = models.CharField(max_length=50 , choices=plan_duration)
    status          = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + "Price: " + str(self.price)
    

class Purchase_History(models.Model):
    user_id             = models.ForeignKey(User , on_delete=models.CASCADE)
    plan_id             = models.ForeignKey(Strip_Plan , on_delete=models.CASCADE)
    customer_id         = models.CharField(max_length=100 , null=True,blank=True)
    stripe_id           = models.CharField(max_length=200)
    invoice             = models.CharField(max_length=100 , null=True , blank=True)
    plan_start_date     = models.DateField(null=True , blank=True)
    plan_end_date       = models.DateField(null=True , blank=True)
    plan_auto_renewal   = models.BooleanField(default=False)
    subscripion_id      = models.CharField(max_length=100 , null=True , blank=True)
    subscription_amount = models.IntegerField(null=True , blank=True)
    payment_status      = models.CharField(max_length=20)
    status              = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id.email) + "Plan: " + str(self.plan_id.name)


class Security_Model(models.Model):
    platform = (
        ('android' , 'Android'),
        ('ios' , 'IOS'),
    )
    client_id = models.CharField(max_length=100)
    platform  = models.CharField(max_length=20 , choices=platform , default="Android")
    timezone = models.DateTimeField(null=True , blank=True)

class testing_model(models.Model):
    payload = models.TextField(max_length=1000)
    text = models.CharField(max_length=100)

    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
