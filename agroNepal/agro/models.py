from django.db import models
from user.models import CustomUser
from django.utils.text import slugify
from datetime import timedelta
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
  
#------------------Crop-----------------
class Crop(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.name

#---------Crop Schedule-----------
class CropSchedule(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="schedules")
    day_number = models.PositiveIntegerField(help_text="Kun din ma k garna")
    task = models.TextField(help_text="Watering, Pesticide")

    class Meta:
        ordering = ['day_number']
    
    def __str__(self):
        return f'{self.crop.name} - Day {self.day_number}: {self.task}'
    
#-----------------------user Crop add 'Yo user crop add vana ko chai user la kunai pani crop plant garxa like "Rice hola banana hola" tayo data yo userCropAdd ma store huxa----------------

class UserCropAdd(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_crops")
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="user_crops")
    planted_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    is_task_hidden = models.BooleanField(default=False) 

    def __str__(self):
      return f"{self.user.username} - {self.crop.name} planted crop on {self.planted_date}"
    

    #-----------CropExpense
class CropExpense(models.Model):
    user_crop = models.ForeignKey(UserCropAdd, on_delete=models.CASCADE, related_name="crop_expenses")
    amount = models.FloatField()
    spend_date = models.DateField()
    note = models.TextField(blank=True, null=True, help_text="e.g., water, food, pesticide")

    def __str__(self):
        return f"Expense Rs: {self.amount} for {self.user_crop.crop.name}"
    

class CropSale(models.Model):
    user_crop = models.ForeignKey(UserCropAdd, on_delete=models.CASCADE, related_name="crop_sales")
    amount = models.FloatField(help_text="Total income from selling")
    quantity = models.FloatField(blank=True, null=True, help_text="In kg")
    sale_date = models.DateField()
    buyer_name = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-sale_date']

    def __str__(self):
        return f"Sale ₹{self.amount} for {self.user_crop.crop.name} ({self.user_crop.planted_date})"

class CommunityPost(models.Model):
  image = models.ImageField(upload_to="img/UserPost", null=True, blank=True)
  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255, unique=True, blank=True)
  description = models.TextField()
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  create_date = models.DateField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)
  user_share_content = models.TextField()

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = self.generate_unique_slug()
    super().save(*args, **kwargs)
  
  def generate_unique_slug(self):
    base_slug = slugify(self.title)
    slug = base_slug
    num = 1
    while CommunityPost.objects.filter(slug=slug).exists():
      slug = f"{base_slug}-{num}"
      num+=1
    return slug

class CommunityPostComment(models.Model):
  share_knowledge = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='share_comments')
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user.username} comment on {self.share_knowledge}"