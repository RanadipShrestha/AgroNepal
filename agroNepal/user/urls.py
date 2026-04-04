from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),

    # Profile Section
    path('profile/', profile, name="profile"),
    path('edit-profile', editProfile, name="edit-profile"),
    path('change-password/', passwordChange, name="change-password"),
]