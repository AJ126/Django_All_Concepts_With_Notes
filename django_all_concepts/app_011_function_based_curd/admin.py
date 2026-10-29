from django.contrib import admin
from app_011_function_based_curd.models import *

# Register your models here.
@admin.register(customer)
class customerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'customerId')
    list_display = ['profilepic', 'name', 'customerId', 'details']