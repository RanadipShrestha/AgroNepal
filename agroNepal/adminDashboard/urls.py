from django.urls import path
from .views import *

urlpatterns = [
   path("", adminDashboard, name="adminDashboard")
]