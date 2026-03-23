from django.urls import path
from .views import *

urlpatterns = [
   path("", adminDashboard, name="admindashboard"),
   path("users/", adminUsers, name="adminUsers"), 
   path("admin-add-user/", adminAddUser, name="adminAddUser"), 
   path("admin-edit-user/<int:user_id>/", adminEditUser, name="adminEditUser"), 
   path("admin-delete-user/", adminDeleteUser, name="adminDeleteUser"), 


   #Crop Ko CRUD Ko
   path("crops/", adminCrops, name="adminCrops"), 
   path("admin-add-crop/", adminAddCrop, name="adminAddCrop"), 
   path("admin-delete-crop/", adminDeleteCrop, name="adminDeleteCrop"),
   path("admin-edit-crop/", adminEditCrop, name="adminEditCrop"),
]