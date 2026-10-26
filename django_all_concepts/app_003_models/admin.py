from django.contrib import admin
from app_003_models.models import *

# Register your models here.
class testDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone']
admin.site.register(testData, testDataAdmin)