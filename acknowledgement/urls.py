from django.urls import path 
from .import views 

urlpatterns = [
    path('',views.acknowledge_page, name='acknowledgement')
]