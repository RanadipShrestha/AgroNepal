from django.urls import path
from .views import *

urlpatterns = [
   path("", adminDashboard, name="admindashboard"),
   path("users/", adminUsers, name="adminUsers"), 
   path("admin-add-user/", adminAddUser, name="adminAddUser"), 
   path("admin-edit-user/<int:user_id>/", adminEditUser, name="adminEditUser"), 
   path("admin-delete-user/", adminDeleteUser, name="adminDeleteUser"), 
]