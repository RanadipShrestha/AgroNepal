from django.contrib import admin
from .models import( Blog, Comment, Contact, Event, Crop, CropSchedule, UserCropAdd, CropSale, ShareKnowledge)
# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Event)
admin.site.register(Crop)
admin.site.register(CropSchedule)
admin.site.register(UserCropAdd)
admin.site.register(CropSale)
admin.site.register(ShareKnowledge)