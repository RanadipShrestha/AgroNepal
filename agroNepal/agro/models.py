from django.db import models
from user.models import CustomUser
from django.utils.text import slugify
import uuid
# Create your models here.

#---------------------------------Blog Model------------------------------------------
class Blog(models.Model):
  image = models.ImageField(upload_to="img/blog", null=True, blank=True)
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)
  description = models.TextField()
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  create_date = models.DateField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)
  blog_content = models.TextField()

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = self.generate_unique_slug()
    super().save(*args, **kwargs)
  
  def generate_unique_slug(self): #generate the unique slug for every blog
    base_slug = slugify(self.title)
    slug = base_slug
    num = 1
    while Blog.objects.filter(slug=slug).exists():
      slug = f"{base_slug}-{num}"
      num+=1
    return slug

#-----------------------------------Comment Model-----------------------------------------
class Comment(models.Model):
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self):
    return f"{self.user.username} comment on {self.blog}"

#--------------------------------------Contact Model--------------------------------------------

class Contact(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  subject = models.CharField(max_length=255)
  email = models.EmailField(max_length=254)
  message = models.TextField()

  def __str__(self):
    return f"{self.first_name} fill the Contact Form with subject: {self.subject}"
  

#-----------------------------------Event Model----------------------------------------------
class Event(models.Model):
  name = models.CharField(max_length=255)
  image = models.ImageField(upload_to="img/blogannouncementImage", null=True, blank=True)
  slug = models.SlugField(unique=True, blank=True)
  price = models.IntegerField()
  description = models.TextField()
  location = models.CharField(max_length=255)
  date = models.DateField()
  eventStartTime = models.TimeField()
  event_duration = models.CharField(max_length=255)
  guest = models.CharField(max_length=50)
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False, null=True, blank=True)
  create_date = models.DateField(auto_now_add=True)
  total_ticket = models.IntegerField()
  available_ticket = models.IntegerField()
  

  def __str__(self):
    return f"The Name of the event is '{self.name}' and the guest is '{self.guest}'"
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = self.generate_unique_slug_event()
    super().save(*args, **kwargs)

  def generate_unique_slug_event(self):
    base_slug = slugify(self.name)
    slug = base_slug
    num = 1
    while Event.objects.filter(slug=slug).exists():
      slug = f"{base_slug}-{num}"
      num+=1
    return slug
  
  def book_ticket(self):
    if self.available_ticket <= 0:
      return False # If tickets available xaina vana return false huxa it means booking failed
    self.available_ticket -= 1
    self.save()
    return True
  
  