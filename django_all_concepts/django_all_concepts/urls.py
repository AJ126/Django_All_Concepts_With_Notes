"""
URL configuration for django_all_concepts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('firstapp/', include('app_001_first.urls')),
    path('templateapp/', include('app_002_template.urls')),
    path('modelapp/', include('app_003_models.urls')),
    path('formapp/', include('app_004_forms.urls')),
    path('modelformapp/', include('app_005_modelForms.urls')),
    path('advtemplateapp/', include('app_006_advance_template.urls')),
    path('sessionapp/', include('app_007_session.urls')),
    path('authapp/', include('app_008_auth.urls')),
    path('mediaapp/', include('app_009_media.urls')),
    path('classApp/', include('app_010_class_based_view.urls')),
    path('functioncardApp/', include('app_011_function_based_curd.urls')),
    path('ormApp/', include('app_012_orm.urls')),
]

# access uploaded images (when user click on the image path on admin then open )
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)