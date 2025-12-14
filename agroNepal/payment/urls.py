from django.urls import path
from . import views

urlpatterns = [
    path('buy-ticket/<int:id>/', views.buy_ticket, name='buy_ticket'),
    path('success/', views.payment_success, name='payment_success'),
    path('failure/', views.payment_failure, name='payment_failure'),
]