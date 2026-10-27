from django.contrib import admin
from django.contrib.sessions.models import Session
# Register your models here.

# show django session model on admin page
admin.site.register(Session)