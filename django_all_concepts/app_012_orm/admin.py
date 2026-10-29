from django.contrib import admin
from app_012_orm.models import *

# Register your models here.
@admin.register(ormInfo)
class ormInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'address', 'date', 'active', 'duration', 'url']