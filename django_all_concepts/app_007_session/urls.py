from django.urls import path
from app_007_session.views import *

urlpatterns = [
    path('setcookie', set_cookie, name ="setcookie"),
    path('checkcookie', check_cookie, name ="checkcookie"),
    path('countpageload', coount_view, name ="countpageload"),
    path('cookieform', show_form, name ="cookieform"),
    path('showdate', show_datetime, name ="showdate"),
    path('formresult', show_form_result, name ="formresult"),
    path('nameview', name_view,name="nameview"),
    path('ageview', age_view,name="ageview"),
    path('gfview', gf_view,name="gfview"),
    path('userresult', result_view,name="userresult"),
    path('thankyouPage', thankyouPage, name="thankyouPage"),
    path('pagecount', page_count, name="pagecount")
]
