from django.urls import path
from app_008_auth.views import *

urlpatterns = [
    path('registerdefault', register_default, name="registerdefault"),
    path('login', login, name="login"),
    path('register', register, name="register"),
    path('logout', logout, name="logout"),
    path('loginrequired', login_required, name="loginrequired")

]
