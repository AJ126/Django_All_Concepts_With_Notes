from django.contrib import admin
from app_013_advance_model.models import *

# Register your models here.
@admin.register(data)
class dataAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']

@admin.register(Userdata)
class UserdataAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact']

@admin.register(parenttable)
class parenttableAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(childtable)
class childtableAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']

@admin.register(parent)
class parentAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(child)
class childAdmin(admin.ModelAdmin):
    list_display = ['name', 'info']

@admin.register(son)
class sonAdmin(admin.ModelAdmin):
    list_display = ['name', 'info', 'details']

@admin.register(detailstest)
class detailstestAdmin(admin.ModelAdmin):
    list_display = ['detail_id', 'address']

@admin.register(info)
class infoAdmin(admin.ModelAdmin):
    list_display = ['info_id', 'city']

@admin.register(test)
class testAdmin(admin.ModelAdmin):
    list_display = ['name','address', 'city']

@admin.register(books)
class booksAdmin(admin.ModelAdmin):
    list_display = ['book','price']

@admin.register(proxyBook)
class proxyBookAdmin(admin.ModelAdmin):
    list_display = ['book','price']

