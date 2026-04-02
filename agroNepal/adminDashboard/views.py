from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.models import CustomUser
from agro.models import Crop, CropSchedule, Contact, Event
from .decorators import admin_only_required
# Create your views here.

@admin_only_required
def adminDashboard(request):
  return render(request, 'adminDashboard/dashboard/dashboard.html')

@admin_only_required
def adminUsers(request):
  users = CustomUser.objects.all().order_by('-date_joined')
  return render(request, 'adminDashboard/dashboard/user/users.html', {'users': users}) 

@admin_only_required
def adminAddUser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        land_address = request.POST.get('land_address', '')

        is_staff = request.POST.get('is_staff') == 'on'
        is_active = request.POST.get('is_active') == 'on'

        if not email or not username or not password:
            messages.error(request, "Required fields missing!", extra_tags="adminAddUser")
            return redirect('adminAddUser')

        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.", extra_tags="adminAddUser")
            return redirect('adminAddUser')

        try:
            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                address=address,
                land_address=land_address,
                is_staff=is_staff,
                is_active=is_active
            )

            messages.success(request, f"User '{username}' created successfully.", extra_tags="adminAddUser")
            return redirect('adminUsers')

        except Exception as e:
            messages.error(request, f"There is an error while creating user", extra_tags="adminAddUser")

    return render(request, 'adminDashboard/dashboard/user/add_user.html')

@admin_only_required
def adminEditUser(request, user_id):
    edit_user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        edit_user.first_name = request.POST.get('first_name')
        edit_user.last_name = request.POST.get('last_name')
        edit_user.username = request.POST.get('username')
        edit_user.email = request.POST.get('email')
        edit_user.phone_number = request.POST.get('phone_number', '')
        edit_user.address = request.POST.get('address', '')
        edit_user.land_address = request.POST.get('land_address', '')
        edit_user.is_staff = request.POST.get('is_staff') == 'true'
        edit_user.is_active = request.POST.get('is_active') == 'true'
        
        try:
            edit_user.save()
            messages.success(request, f"User '{edit_user.username}' updated successfully.", extra_tags="adminAddUser")
            return redirect('adminUsers')
        except:
            messages.error(request, f"Error updating user.", extra_tags="adminAddUser")
            
    return render(request, 'adminDashboard/dashboard/user/edit_user.html', {'edit_user': edit_user})

@admin_only_required
def adminDeleteUser(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_to_delete = get_object_or_404(CustomUser, id=user_id)
        if user_to_delete == request.user:
            messages.error(request, "You cannot delete yourself", extra_tags="adminAddUser")
        else:
            username = user_to_delete.username
            user_to_delete.delete()
            messages.success(request,"user deleted successfully", extra_tags="adminAddUser")
    return redirect('adminUsers')

@admin_only_required
def adminCrops(request):
    crops = Crop.objects.prefetch_related('schedules').all().order_by('-id')
    return render(request, 'adminDashboard/dashboard/crop/crops.html', {'crops': crops})

@admin_only_required
def adminAddCrop(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if not name:
            messages.error(request, "Crop name is required")
            return redirect('adminCrops')

        crop = Crop.objects.create(name=name, description=description)

        day_numbers = request.POST.getlist('schedule_day[]')
        tasks = request.POST.getlist('schedule_task[]')

        for day, task in zip(day_numbers, tasks):
            if day and task:
                CropSchedule.objects.create(
                    crop=crop,
                    day_number=int(day),
                    task=task
                )

        messages.success(request, f"Crop '{name}' added successfully.", extra_tags="admincrop")

    return redirect('adminCrops')

@admin_only_required
def adminEditCrop(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        #Validation
        if not name:
            messages.error(request, "Crop name is required")
            return redirect('adminCrops')

        crop = get_object_or_404(Crop, id=crop_id)

        # Update crop
        crop.name = name
        crop.description = description
        crop.save()

        #Delete old schedules
        crop.schedules.all().delete()

        # Add new schedules
        day_numbers = request.POST.getlist('schedule_day[]')
        tasks = request.POST.getlist('schedule_task[]')

        for day, task in zip(day_numbers, tasks):
            if day and task:
                CropSchedule.objects.create(
                    crop=crop,
                    day_number=int(day),
                    task=task
                )

        messages.success(request, f"Crop '{name}' updated successfully.")

    return redirect('adminCrops')

@admin_only_required
def adminDeleteCrop(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        crop = get_object_or_404(Crop, id=crop_id)
        crop_name = crop.name
        crop.delete()
        messages.success(request, "Crop deleted successfully.")
    return redirect('adminCrops')

@admin_only_required
def adminContacts(request):
    contacts = Contact.objects.all().order_by('-id')
    context = {
        'contacts':contacts
    }
    return render(request, "adminDashboard/dashboard/contact/contacts.html", context)

@admin_only_required
def adminDeleteContact(request):
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id)
        subject = contact.subject
        contact.delete()
        messages.success(request, f"Contact message '{subject}' deleted successfully.", extra_tags="deleteContact")
    return redirect('adminContacts')


@admin_only_required
def adminEvents(request):
    events = Event.objects.all().order_by('-create_date')
    context = {
        'events': events
    }
    return render(request, 'adminDashboard/dashboard/event/events.html', context)

@admin_only_required
def adminAddEvent(request):
    if request.method == "POST":
        name = request.POST.get('name')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        description = request.POST.get('description')
        location = request.POST.get('location')
        date = request.POST.get('date')
        eventStartTime = request.POST.get('eventStartTime')
        event_duration = request.POST.get('event_duration')
        guest = request.POST.get('guest')
        total_ticket = request.POST.get('total_ticket')

        try:
            Event.objects.create(
                name=name,
                image=image,
                price=price,
                description=description,
                location=location,
                date=date,
                eventStartTime=eventStartTime,
                event_duration=event_duration,
                guest=guest,
                total_ticket=total_ticket,
                available_ticket=total_ticket,
                author=request.user
            )
            messages.success(request, "New Event Added Successfully", extra_tags="eventAdd")
            return redirect('adminEvents')

        except:
            messages.error(request, 'There is issues in the enter data please correct that', extra_tags="eventAdd")
    return render(request, 'adminDashboard/dashboard/event/add_event.html')