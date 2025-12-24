from django.urls import path
from .views import *

urlpatterns = [
    path("", userDashboard, name="userdashboard"), 
]