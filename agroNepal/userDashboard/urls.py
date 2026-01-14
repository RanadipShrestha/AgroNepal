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
]