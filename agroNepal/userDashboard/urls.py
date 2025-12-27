from django.urls import path
from .views import *

urlpatterns = [
    path("", userDashboard, name="userdashboard"), 
   path('crop/', addCrop, name='crop'),
    path('delete-crop/', deleteUserCrop, name='delete_crop'),
]