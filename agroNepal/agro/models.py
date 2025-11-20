from django.db import models
from user.models import CustomUser
from django.utils.text import slugify
# Create your models here.

class Blog(models.Model):
  image = models.ImageField(upload_to="img/blog", null=True, blank=True)
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, blank=True)
  description = models.TextField()
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="blogs")
  create_date = models.DateField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)
  blog_content = models.TextField()

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
    while Blog.objects.filter(slug=slug).exists():
      num+=1
    return slug
