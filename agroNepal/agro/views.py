from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment, Contact, Event
from django.db.models import Q
from django.contrib import messages
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
  if request.method == "POST":
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")

    Contact.objects.create(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)

    messages.success(request, "Thank you for your feedback! We will get back to you soon.",extra_tags='contact-success')
    return redirect('contact')
  
  
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



def blog_detail(request, slug):
  blog = get_object_or_404(Blog, slug=slug)
  comments = blog.comments.all()
  context = {
    'blog':blog,
    'comments':comments,
  }
  return render(request, 'pages/blog/readmoreBlog.html', context)


def add_comment(request, slug):
  if request.method == "POST":
    blog = get_object_or_404(Blog, slug=slug)
    comment_text = request.POST.get("comment_text")

    if comment_text:
      Comment.objects.create(
        blog=blog,
        user = request.user,
        text = comment_text
      )
      messages.success(request, "Comment done successfully", extra_tags="commentSuccess")
    else:
      messages.error(request, "The comment fields is empty", extra_tags="emptyComment")
    
  return redirect("readMoreBlog", slug=slug)


def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Check if user is the comment owner or staff
        if request.user == comment.user or request.user.is_staff:
            blog_slug = comment.blog.slug
            comment.delete()
            messages.success(request, 'Comment deleted successfully!')
            return redirect('readMoreBlog', slug=blog_slug)
        else:
            messages.error(request, 'You do not have permission to delete this comment.')
            return redirect('readMoreBlog', slug=comment.blog.slug)
    
    return redirect('blog')


def event(request):
  events = Event.objects.all()
  context = {
    "events":events
  }
  return render(request, "pages/event/event.html", context)


from django.shortcuts import render

def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

