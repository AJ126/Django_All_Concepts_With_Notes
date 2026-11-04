from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)

@admin.register(AdminPageModel)
class AdminPageModelAdmin(admin.ModelAdmin):
    list_display = ('name',  'email', 'message', 'info', 'phone', 'created_at', 'status')
    search_fields = ('name', 'email', 'message', 'info', 'phone')
    list_filter = ('created_at', 'status')
    ordering = ('-created_at',)
    prepopulated_fields = {'info': ('name',)}  # Prepopulate the 'info' field based on the 'name' field
    raw_id_fields = ('user_id',)  # Display the 'user_id' field as a raw ID field
    # readonly_fields = ('created_at',)  # Make the 'created_at' field read-only in the admin interface
    date_hierarchy = 'created_at'  # Enable date hierarchy navigation based on the 'created_at' field
