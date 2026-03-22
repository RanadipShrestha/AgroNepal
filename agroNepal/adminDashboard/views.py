from django.shortcuts import render, redirect, get_object_or_404
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
            messages.error(request, f"There is an error while creating user", extra_tags="adminAddUser")

    return render(request, 'adminDashboard/dashboard/user/add_user.html')

def adminEditUser(request, user_id):
    edit_user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        edit_user.first_name = request.POST.get('first_name')
        edit_user.last_name = request.POST.get('last_name')
        edit_user.username = request.POST.get('username')
        edit_user.email = request.POST.get('email')
        edit_user.phone_number = request.POST.get('phone_number', '')
        edit_user.address = request.POST.get('address', '')
        edit_user.land_address = request.POST.get('land_address', '')
        edit_user.is_staff = request.POST.get('is_staff') == 'true'
        edit_user.is_active = request.POST.get('is_active') == 'true'
        
        try:
            edit_user.save()
            messages.success(request, f"User '{edit_user.username}' updated successfully.", extra_tags="adminAddUser")
            return redirect('adminUsers')
        except:
            messages.error(request, f"Error updating user.", extra_tags="adminAddUser")
            
    return render(request, 'adminDashboard/dashboard/user/edit_user.html', {'edit_user': edit_user})

def adminDeleteUser(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_to_delete = get_object_or_404(CustomUser, id=user_id)
        if user_to_delete == request.user:
            messages.error(request, "You cannot delete yourself", extra_tags="adminAddUser")
        else:
            username = user_to_delete.username
            user_to_delete.delete()
            messages.success(request,"user deleted successfully", extra_tags="adminAddUser")
    return redirect('adminUsers')