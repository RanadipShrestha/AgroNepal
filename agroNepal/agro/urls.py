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
  path('edit_blog_comment/<int:comment_id>/edit/', edit_blog_comment, name='edit_blog_comment'),
  path("event/", event, name="event"),
  
  path("community_public_post/", community_public_post, name="community_public_post"),
  path("community_public_post_detail/<slug:slug>/", community_public_post_detail, name="community_public_post_detail"),
  path("community_public_post_comment/<slug:slug>/comment/", community_public_post_comment, name="community_public_post_comment"),
  path("delete_commmunity_post_comment/<int:comment_id>/delete/", delete_commmunity_post_comment, name="delete_commmunity_post_comment"),
  path("edit_community_post_comment/<int:comment_id>/edit/", edit_community_post_comment, name="edit_community_post_comment"),
]