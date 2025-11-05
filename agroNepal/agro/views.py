from django.shortcuts import render

# Create your views here.

def index(request):
  return render(request, "pages/index.html")

def login(request):
  return render(request, 'accounts/login.html')

def register(request):
  return render(request, 'accounts/register.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
   return render(request, "pages/contact.html")

def event(request):
  return render(request, "pages/event.html")