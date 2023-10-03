from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *




class UserAccountAdmin(UserAdmin):
    list_display=('email','username')
    search_fields=('email','username')
    readonly_fields=('id',)
    filter_horizontal=()
    list_filter=('active',)
    fieldsets=(
        ('Personal',
            {
                'fields':('username','email')
            }),
        (
            'Details',
            {
                'fields':('active','staff','admin')
            }),
            ('Permissions', {'fields': (
            'groups','user_permissions',
            )}),   
    )

admin.site.register(User,UserAccountAdmin) 