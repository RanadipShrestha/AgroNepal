from django.contrib import messages
from django.shortcuts import redirect

def admin_only_required(view_func):  
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.', extra_tags="adminOnly")
            return redirect('login')
        
        # If NOT admin no permission
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(
                request,
                'You do not have permission to access Admin Dashboard. Please login Admin account.',
                extra_tags="adminOnly"
            )
            return redirect('login') 
        
        return view_func(request, *args, **kwargs)
    
    return wrapper