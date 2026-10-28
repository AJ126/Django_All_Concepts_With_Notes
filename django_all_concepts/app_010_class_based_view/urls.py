from django.urls import path
from app_010_class_based_view.views import *

urlpatterns = [
    path('classBasedView/', show_simple_class.as_view(), name="classBasedView"),
    path('templateview/', templateView.as_view(), name="templateview"),
    path('listview/', listView.as_view(), name="listview"),
    path('detailview/<slug:pk>/', detailViewClass.as_view(), name="detailview"),
    path('createview/', createRecord.as_view(), name="createview"),
    path('updaterecord/<slug:pk>/', updateRecord.as_view(), name="updaterecord"),
    path('deleterecord/<slug:pk>/', deleteRecord.as_view(), name="deleterecord"),
]
