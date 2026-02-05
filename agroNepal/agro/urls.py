from django.urls import path
from .views import *
urlpatterns = [
  path('', index, name="index"),
  path("about/", about, name="about"),
  path("contact/", contact, name="contact"),
  path("blog/", blog, name="blog"),
  path("blog/<slug:slug>/", blog_detail, name="readMoreBlog"),
  path("blog/<slug:slug>/comment/", add_comment, name="add_comment"),
  path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
  path("event/", event, name="event"),
]