from django.shortcuts import render
from user.models import CustomUser

# Create your views here.
def adminDashboard(request):
  return render(request, 'adminDashboard/dashboard/dashboard.html')

def adminUsers(request):
  users = CustomUser.objects.all().order_by('-date_joined')
  return render(request, 'adminDashboard/dashboard/user/users.html', {'users': users}) 