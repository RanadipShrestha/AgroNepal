from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            
            user = authenticate(request, email=email, password=password)
            if user:
                auth_login(request, user)
                return redirect("login")
        else:
            if form.errors.get('password2'):
                messages.error(request, "The passwords you entered do not match. Please try again.")
            elif form.errors.get('username'):
                messages.error(request, "This username is already taken. Please choose a different one.")
            elif form.errors.get('email'):
                messages.error(request, "This email is already registered.")
            elif form.errors.get('password1'):
                messages.error(request, "Your password is too weak. ")
            elif form.errors.get('phone_number'):
                messages.error(request, "Phone number must contain only digits.")
            else:
                messages.error(request, "Please fill in all required fields.")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('admindashboard')
            else:
                return redirect('userdashboard')
        else:
            messages.error(request, 'Invalid email or password.', extra_tags="invalidPasswordoremail")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash


def profile(request):
    return render(request, "userProfile/profile.html")



def editProfile(request):
    user = request.user

    if request.method == "POST":
        # Getting updated data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        land_address = request.POST.get('land_address')

        CustomUser = get_user_model()

        # Check username uniqueness
        if CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, "Username already exists.", extra_tags="userProfileUpdate")
            return redirect('edit-profile')

        # Check email uniqueness
        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, "Email already exists.", extra_tags="userProfileUpdate")
            return redirect('edit-profile')

        # Update user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.address = address
        user.land_address = land_address

        user.save()

        messages.success(request, "Your Profile Updated Successfully", extra_tags="userProfileUpdate")
        return redirect('profile')

    # GET request → show form
    return render(request, "userProfile/edit_profile.html", {"user": user})


def passwordChange(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!', extra_tags="userProfileUpdate")
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.', extra_tags="userProfileUpdate")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userProfile/change_password.html', {
        'form': form
    })
