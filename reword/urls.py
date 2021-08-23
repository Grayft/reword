"""reword URL Configuration"""
from ast import increment_lineno

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('learn.urls')),
]
