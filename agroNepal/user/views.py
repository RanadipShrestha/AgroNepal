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
            messages.error(request, "Please Enter all fields", extra_tags="fields-message")
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
                return redirect('admin')
            else:
                return redirect('userDashboard')

        else:
            messages.error(request, 'Invalid email or password.', extra_tags="invalidPasswordoremail")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')


