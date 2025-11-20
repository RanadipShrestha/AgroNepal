from django.urls import path
from .views import *
urlpatterns = [
  path('', index, name="index"),
  path("login/", login, name="login"),
  path("register/", register, name="register"),
  path("about/", about, name="about"),
  path("contact/", contact, name="contact"),
  path("blog/", blog, name="blog"),
  path("event/", event, name="event"),
]