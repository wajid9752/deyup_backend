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

@admin.register(Strip_Plan)
class Strip_PlanAdmin(admin.ModelAdmin):
    list_display = (
        "plan_duration",
        "name",
        "description",
        "image",
        "price",
        "duration",
        "status",
        "created_at",
        "updated_at"
    )



@admin.register(Purchase_History)
class Purchase_HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "plan_id",
        "transaction_id",
        "plan_start_date",
        "plan_end_date",
        "plan_auto_renewal",
        "status",
        "created_at",
        "updated_at"
    )


@admin.register(Security_Model)
class Security_ModelAdmin(admin.ModelAdmin):
    list_display=(
        "client_id",
        "platform",
        "timezone"
    )

