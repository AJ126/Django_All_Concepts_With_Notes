from django.contrib import admin
from app_010_class_based_view.models import *
# Register your models here.
@admin.register(testInfo)
class testInfoAdmin(admin.ModelAdmin):
    list_display=['name','address']