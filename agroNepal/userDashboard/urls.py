from django.urls import path
from . views import *

urlpatterns = [
    path("", userDashboard, name="userdashboard"), 
    path('crop/', addCrop, name='crop'),
    path('delete-crop/', deleteUserCrop, name='delete_crop'),
    path('cropexpense/', cropExpense, name='cropExpense'),
    path('delete-expense/', deleteExpense, name='deleteExpense'),
    path('delete-crop-expenses/', deleteCropExpenses, name='deleteCropExpenses'),
    path("edit-expense/", edit_expense, name="editExpense"),

    # Sales Management URLs
    path('crop-sales/', cropSales, name='cropSales'),
    path('edit-sale/', editSale, name='editSale'),
    path('delete-sale/', deleteSale, name='deleteSale'),
    path('delete-crop-sales/', deleteCropSales, name='deleteCropSales'),

    # Knowledge Share URLs
    path('share-knowledge/', userShareKnowledge, name='userShareKnowledge'),
    path('edit-share-knowledge/', editShareKnowledge, name='editShareKnowledge'),
    path('delete-share-knowledge/', deleteShareKnowledge, name='deleteShareKnowledge'),

    # Profile Section
    path('profile/', profile, name="profile"),
    path('edit-profile', userEditProfile, name="edit-profile"),
    path('userUpdatedProfile', userUpdatedProfile, name="userUpdatedProfile"),

    # Ticket
    path("userTickets/", userTickets, name="userTickets")
]