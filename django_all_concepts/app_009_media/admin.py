from django.contrib import admin
from app_009_media.models import *
# Register your models here.
@admin.register(media)
class mediaAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']