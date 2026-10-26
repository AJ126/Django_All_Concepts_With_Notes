from django.contrib import admin
from app_006_advance_template.models import *

# Register your models here.
class userInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'data', 'details', 'date']
admin.site.register(userInfo, userInfoAdmin)