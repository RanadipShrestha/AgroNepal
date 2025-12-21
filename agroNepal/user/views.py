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
                return redirect("index")
            else:
                return redirect("login")
        else:
            if form.errors.get('password2'):
                messages.error(request, "The passwords you entered do not match. Please try again.")
            elif form.errors.get('username'):
                messages.error(request, "This username is already taken. Please choose a different one.")
            elif form.errors.get('email'):
                messages.error(request, "This email is already registered.")
            elif form.errors.get('password1'):
                messages.error(request, "Your password is too weak. Please use at least 8 characters with letters and numbers.")
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
                return redirect('index')
            else:
                return redirect('userDashboard')

        else:
            messages.error(request, 'Invalid email or password.', extra_tags="invalidPasswordoremail")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')



