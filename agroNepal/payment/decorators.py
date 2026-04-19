from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
def user_only_payment(view_func):
    """Decorator to allow only non-staff users"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first. To buy ticket.', extra_tags="userOnly")
            return redirect('login')
        
        # Check if user IS Admin
        if request.user.is_staff or request.user.is_superuser:
            messages.error(request, 'You do not have permission to buy ticket. Please login User account.',  extra_tags="userOnly")
            logout(request)
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper