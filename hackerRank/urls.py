from django.contrib import admin
from django.urls import path
from .views import index,delete,load_data, submit
urlpatterns = [
    path('index/', index, name = 'index'),
    path('submit/',submit,name='submit'),
    path('delete/',delete),
    path('loadData/',load_data)
]