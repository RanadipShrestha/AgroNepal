from django.urls import path
from .views import *

urlpatterns = [
   path("", adminDashboard, name="admindashboard"),
   path("users/", adminUsers, name="adminUsers"), 
   path("admin-add-user/", adminAddUser, name="adminAddUser"), 
]