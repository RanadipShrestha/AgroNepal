from django.urls import path
from .views import *

urlpatterns = [
   path("", adminDashboard, name="admindashboard"),
    path("users/", adminUsers, name="adminUsers"), 
]