from django.contrib import admin
from app_015_signals.models import *

# Register your models here.
@admin.register(customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer_id']

@admin.register(customerInfo)
class customerInfoAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'detail']