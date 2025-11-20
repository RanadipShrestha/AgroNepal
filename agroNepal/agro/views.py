from django.shortcuts import render
from .models import Blog
from django.db.models import Q
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

def blog(request):
  search_data = request.GET.get('search', '')
  
  if search_data:
   blogs = Blog.objects.filter(
    Q(title__icontains=search_data) | 
    Q(description__icontains=search_data) |
    Q(blog_content__icontains=search_data)
   )
  else:
   blogs = blogs = Blog.objects.raw("SELECT * FROM agro_blog")

  recent_blogs = Blog.objects.all()[:5]
  context = {
    'blogs': blogs,
    'recent_blogs':recent_blogs,
    'search_data': search_data,
   }
  return render(request, "pages/blog/blog.html", context)

def event(request):
  return render(request, "pages/event.html")