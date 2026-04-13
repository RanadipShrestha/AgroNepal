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

   # Manage Contacts
    path("contacts/", adminContacts, name="adminContacts"),
    path("delete-contact/", adminDeleteContact, name="adminDeleteContact"),

    # Manage Events
    path("events/", adminEvents, name="adminEvents"),
    path("events/add/", adminAddEvent, name="adminAddEvent"),
    path("events/edit/<int:event_id>/", adminEditEvent, name="adminEditEvent"),
    path("delete-event/", adminDeleteEvent, name="adminDeleteEvent"),

    # Manage Blogs
    path("blogs/", adminBlogs, name="adminBlogs"),
    path("blogs/add/", adminAddBlog, name="adminAddBlog"),
    path("blogs/edit/<int:blog_id>/", adminEditBlog, name="adminEditBlog"),
    path("delete-blog/", adminDeleteBlog, name="adminDeleteBlog"),

    # Manage Tickets
    path("tickets/", adminTickets, name="adminTickets"),


    # Manage Community Posts
    path("community-posts/", adminCommunityPosts, name="adminCommunityPosts"),
    path("community-posts/add/", adminAddCommunityPost, name="adminAddCommunityPost"),
    path("community-posts/edit/<int:post_id>/", adminEditCommunityPost, name="adminEditCommunityPost"),
    path("delete-post/", adminDeleteCommunityPost, name="adminDeleteCommunityPost"),

    #User expesne, sale and crop planted record
    path("adminUserExpenses/", adminUserExpenses, name="adminUserExpenses"),
    path("adminUserSales/", adminUserSales, name="adminUserSales"),
    path("adminUserPlantedCrops/", adminUserPlantedCrops, name="adminUserPlantedCrops"),
    path("adminUserPlantedCrops/edit/<int:crop_id>/", adminEditUserPlantedCrop, name="adminEditUserPlantedCrop"),
    path("adminUserPlantedCrops/delete/", adminDeleteUserPlantedCrop, name="adminDeleteUserPlantedCrop"),
]