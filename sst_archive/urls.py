from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('data_access.urls')),
    path('', include('frontend.urls', namespace='')),
]
