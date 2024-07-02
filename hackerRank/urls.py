from django.contrib import admin
from django.urls import path
from .views import index,delete
urlpatterns = [
    path('index/',index,name='index'),
    path('delete/',delete)
]