from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from agro.models import Crop
from agro.models import UserCropAdd


# Create your views here.

def userDashboard(request):
  return render(request, "userDashboard/Dashboard/dashboard.html")

#----------------------------------Crop Page--------------
#----------------------------------Crop Page--------------
def addCrop(request):
  if request.method == "POST":
    crop_id = request.POST.get('crop')
    planted_date = request.POST.get('planted_date')
    notes = request.POST.get('notes', '')

    try:
      crop = Crop.objects.get(id=crop_id)
      UserCropAdd.objects.create(
        user=request.user,
        crop=crop,
        planted_date=planted_date,
        notes=notes
      )
      messages.success(request, "Crop Added Successfully", extra_tags="cropAddedSuccessfully")
      return redirect("crop")
    except Crop.DoesNotExist:
      messages.error(request, 'Invalid Crop Selected.')
      return redirect("crop")
    except Exception as e:
      messages.error(request, f"Error adding Crop: {str(e)}")
      return redirect("crop")
  
  crops = Crop.objects.all()
  user_crop = UserCropAdd.objects.filter(user=request.user).select_related('crop').order_by('-planted_date')
  
  context = {
      'crops': crops,
      'user_crops': user_crop,
  }
  return render(request, "userDashboard/dashboard/plantedCrop.html", context)


def deleteUserCrop(request):
  if request.method == "POST":
    crop_id = request.POST.get('crop_id')  # Get from POST data, not URL
    user_crop = get_object_or_404(UserCropAdd, id=crop_id, user=request.user)
    crop_name = user_crop.crop.name
    user_crop.delete()
    messages.success(request, f"{crop_name} Deleted Successfully", extra_tags="cropDeletedSuccessfully")
  
  return redirect("crop")