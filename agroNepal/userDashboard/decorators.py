from django.contrib import messages
from django.shortcuts import redirect
def user_only_required(view_func):
    """Decorator to allow only non-staff users"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('login')
        
        # Check if user IS staff OR superuser - redirect to login
        if request.user.is_staff or request.user.is_superuser:
            messages.error(request, 'You do not have permission to access user dashboard.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper