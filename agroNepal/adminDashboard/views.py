from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import CustomUser

# Create your views here.
def adminDashboard(request):
  return render(request, 'adminDashboard/dashboard/dashboard.html')

def adminUsers(request):
  users = CustomUser.objects.all().order_by('-date_joined')
  return render(request, 'adminDashboard/dashboard/user/users.html', {'users': users}) 

def adminAddUser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        land_address = request.POST.get('land_address', '')

        is_staff = request.POST.get('is_staff') == 'on'
        is_active = request.POST.get('is_active') == 'on'

        if not email or not username or not password:
            messages.error(request, "Required fields missing!", extra_tags="adminAddUser")
            return redirect('adminAddUser')

        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.", extra_tags="adminAddUser")
            return redirect('adminAddUser')

        try:
            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                address=address,
                land_address=land_address,
                is_staff=is_staff,
                is_active=is_active
            )

            messages.success(request, f"User '{username}' created successfully.", extra_tags="adminAddUser")
            return redirect('adminUsers')

        except Exception as e:
            messages.error(request, f"Error creating user: {e}", extra_tags="adminAddUser")

    return render(request, 'adminDashboard/dashboard/user/add_user.html')
        