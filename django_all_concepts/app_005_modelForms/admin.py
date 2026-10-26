from django.contrib import admin
from app_005_modelForms.models import *
# Register your models here.

class demoDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'city', 'address']
admin.site.register(demoData, demoDataAdmin)

class dateModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
admin.site.register(dateModel, dateModelAdmin)