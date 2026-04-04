from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from collections import defaultdict
from datetime import datetime, date, timedelta
from agro.models import CropExpense, UserCropAdd, Crop, CommunityPost, CustomUser, CropSale
from payment.models import PurchaseTicket
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.db.models import Sum
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import user_only_required
# Create your views here.

@user_only_required
def userDashboard(request):
  total_crops = UserCropAdd.objects.filter(user=request.user).count()
  total_expense = CropExpense.objects.filter(user_crop__user = request.user).aggregate(Sum('amount'))['amount__sum'] or 0
  total_sales = CropSale.objects.filter(user_crop__user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
  total_posts = CommunityPost.objects.filter(author=request.user).count()
  total_tickets = PurchaseTicket.objects.filter(user=request.user).count()
  recent_posts = CommunityPost.objects.filter(author=request.user).order_by('-create_date')[:3]
  recent_crops = UserCropAdd.objects.filter(user=request.user).select_related('crop').order_by('-planted_date')[:5]
  context = {
      "total_crops":total_crops,
      'total_expense':total_expense,
      'total_sales':total_sales,
      'total_posts':total_posts,
      'total_tickets':total_tickets,
      'recent_posts':recent_posts,
      'recent_crops':recent_crops
  }
  return render(request, "userDashboard/Dashboard/dashboard.html", context)

#----------------------------------Crop Page--------------
@user_only_required
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
  return render(request, "userDashboard/Dashboard/plantedCrop.html", context)

@user_only_required
def deleteUserCrop(request):
  if request.method == "POST":
    crop_id = request.POST.get('crop_id')  # Get from POST data, not URL
    user_crop = get_object_or_404(UserCropAdd, id=crop_id, user=request.user)
    crop_name = user_crop.crop.name
    user_crop.delete()
    messages.success(request, f"{crop_name} Deleted Successfully", extra_tags="cropDeletedSuccessfully")
  
  return redirect("crop")

@user_only_required
def editUserCrop(request):
    if request.method == "POST":
        user_crop_id = request.POST.get('user_crop_id')
        crop_id = request.POST.get('crop')
        planted_date = request.POST.get('planted_date')
        notes = request.POST.get('notes', '')

        if not user_crop_id or not crop_id:
            messages.error(request, "Failed to identify the crop record or the new crop type.")
            return redirect("crop")

        try:
            user_crop = get_object_or_404(UserCropAdd, id=user_crop_id, user=request.user)
            crop = get_object_or_404(Crop, id=crop_id)
            
            user_crop.crop = crop
            user_crop.planted_date = planted_date
            user_crop.notes = notes
            user_crop.save()
            
            messages.success(request, f"{crop.name} Updated Successfully", extra_tags="cropUpdatedSuccessfully")
        except Exception as e:
            messages.error(request, f"Error updating crop: {str(e)}")
            
    return redirect("crop")

@user_only_required
def cropExpense(request):
    if request.method == 'POST': 
        # Handle adding new expense
        user_crop_id = request.POST.get('user_crop')
        amount = request.POST. get('amount')
        spend_date = request.POST.get('spend_date')
        note = request.POST.get('note', '')
        
        try:
            user_crop = get_object_or_404(UserCropAdd, id=user_crop_id, user=request.user)
            
            # Create the expense
            CropExpense.objects.create(
                user_crop=user_crop,
                amount=amount,
                spend_date=spend_date,
                note=note
            )
            
            messages.success(request, f'Expense for {user_crop.crop.name} added successfully!')
            return redirect('cropExpense')
            
        except Exception as e:
            messages. error(request, f'Error adding expense: {str(e)}')
            return redirect('cropExpense')
    
    user_crops_with_expenses = UserCropAdd.objects.filter(
        user=request.user,
        crop_expenses__isnull=False  # Changed from cropexpense to crop_expenses
    ).distinct().select_related('crop').prefetch_related('crop_expenses').order_by('crop__name', '-planted_date')
    
    # Structure data for template:  each user_crop is separate
    crops_data = []
    for user_crop in user_crops_with_expenses:
        expenses = user_crop.crop_expenses.all().order_by('-spend_date')  # Changed here too
        crops_data.append({
            'user_crop_id': user_crop.id,
            'crop_name': user_crop.crop. name,
            'planted_date': user_crop.planted_date,
            'notes': user_crop.notes,  
            'expenses': expenses
        })
    
    # Get all user's planted crops for the form dropdown
    all_user_crops = UserCropAdd.objects.filter(user=request. user).select_related('crop').order_by('-planted_date')
    
    context = {
        'crops_data': crops_data,
        'user_crops':  all_user_crops,
    }
    return render(request, "userDashboard/Dashboard/crop_expense_management.html", context)


#Delete a single Expense
@user_only_required
def deleteExpense(request):
    if request.method == 'POST': 
        expense_id = request. POST.get('expense_id')
        expense = get_object_or_404(CropExpense, pk=expense_id, user_crop__user=request.user)
        crop_name = expense.user_crop.crop.name
        expense.delete()
        messages.success(request, f'Expense for {crop_name} deleted successfully.')
    return redirect('cropExpense')

#Delect all the Expense
def deleteCropExpenses(request):
    if request.method == 'POST': 
        crop_id = request.POST.get('crop_id')
        try:
            user_crop = get_object_or_404(UserCropAdd, id=crop_id, user=request.user)

            CropExpense.objects.filter(user_crop=user_crop).delete()
            messages.success(request, 'All expenses Deleted ', extra_tags="expense_delete")
                
        except Exception as e:
            messages.error(request, f'Error deleting expenses: {str(e)}')
    
    return redirect('cropExpense')

@user_only_required
def edit_expense(request):
    if request.method == "POST":
        expense_id = request.POST.get("expense_id")

        expense = get_object_or_404(
            CropExpense,
            id=expense_id,
            user_crop__user=request.user
        )

        expense.amount = request.POST.get("amount")
        expense.spend_date = request.POST.get("spend_date")
        expense.note = request.POST.get("note", "")
        expense.save()

        messages.success(request, "Expense updated successfully.")

    return redirect("cropExpense")

@user_only_required
def cropSales(request):
    if request.method == 'POST':
        # Handle adding new sale
        user_crop_id = request.POST.get('user_crop')
        amount = request.POST.get('amount')
        quantity = request.POST.get('quantity', None)
        sale_date = request.POST.get('sale_date')
        buyer_name = request.POST.get('buyer_name', '')
        note = request.POST.get('note', '')
        
        try:
            user_crop = get_object_or_404(UserCropAdd, id=user_crop_id, user=request.user)
            
            # Create the sale
            CropSale.objects.create(
                user_crop=user_crop,
                amount=amount,
                quantity=quantity if quantity else None,
                sale_date=sale_date,
                buyer_name=buyer_name,
                note=note
            )
            
            messages.success(request, f'Sale for {user_crop.crop.name} added successfully!')
            return redirect('cropSales')
            
        except Exception as e:
            messages.error(request, f'Error adding sale: {str(e)}')
            return redirect('cropSales')
    
    # GET request - Display sales
    # Get all user crops with their sales
    user_crops_with_sales = UserCropAdd.objects.filter(
        user=request.user,
        crop_sales__isnull=False
    ).distinct().select_related('crop').prefetch_related('crop_sales').order_by('crop__name', '-planted_date')
    
    # Structure data for template: each user_crop is separate
    crops_data = []
    for user_crop in user_crops_with_sales:
        sales = user_crop.crop_sales.all().order_by('-sale_date')
        crops_data.append({
            'user_crop_id': user_crop.id,
            'crop_name': user_crop.crop.name,
            'planted_date': user_crop.planted_date,
            'notes': user_crop.notes,
            'sales': sales
        })
    
    # Get all user's planted crops for the form dropdown
    all_user_crops = UserCropAdd.objects.filter(user=request.user).select_related('crop').order_by('-planted_date')
    
    context = {
        'crops_data': crops_data,
        'user_crops': all_user_crops,
    }
    return render(request, "userDashboard/Dashboard/sale_expense_management.html", context)

@user_only_required
def editSale(request):
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        amount = request.POST.get('amount')
        quantity = request.POST.get('quantity', None)
        sale_date = request.POST.get('sale_date')
        buyer_name = request.POST.get('buyer_name', '')
        note = request.POST.get('note', '')
        
        try:
            sale = get_object_or_404(CropSale, id=sale_id, user_crop__user=request.user)
            sale.amount = amount
            sale.quantity = quantity if quantity else None
            sale.sale_date = sale_date
            sale.buyer_name = buyer_name
            sale.note = note
            sale.save()
            
            messages.success(request, 'Sale updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating sale: {str(e)}')
    
    return redirect('cropSales')

@user_only_required
def deleteSale(request):
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        
        try:
            sale = get_object_or_404(CropSale, id=sale_id, user_crop__user=request.user)
            crop_name = sale.user_crop.crop.name
            sale.delete()
            
            messages.success(request, f'Sale for {crop_name} deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting sale: {str(e)}')
    
    return redirect('cropSales')

@user_only_required
def deleteCropSales(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        
        try:
            user_crop = get_object_or_404(UserCropAdd, id=crop_id, user=request.user)
            crop_name = user_crop.crop.name
            
            # Delete all sales for this crop
            deleted_count = CropSale.objects.filter(user_crop=user_crop).delete()[0]
            
            messages.success(request, f'All {deleted_count} sales for {crop_name} deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting sales: {str(e)}')
    
    return redirect('cropSales')

#--------------------------------------------------------------------------------
@user_only_required
def userShareKnowledge(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_share_content = request.POST.get('user_share_content')
        image = request.FILES.get('image', None)

        try:
            share = CommunityPost.objects.create(
                title=title,
                description=description,
                user_share_content=user_share_content,
                author=request.user,
                image=image
            )
            messages.success(request, f'Commpunity Post created successfully!', extra_tags="shareKnowledgeSuccess")
            return redirect('userShareKnowledge')
        except Exception as e:
            messages.error(request, f'Error creating Knowledge Share: {str(e)}', extra_tags="shareKnowledgeError")
            return redirect('userShareKnowledge')
    
    shares = CommunityPost.objects.filter(author=request.user).order_by('-create_date')
    
    context = {
        'shares': shares,
    }
    return render(request, "userDashboard/Dashboard/community_post.html", context)

@user_only_required
def editShareKnowledge(request):
    if request.method == 'POST':
        share_id = request.POST.get('share_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_share_content = request.POST.get('user_share_content')
        image = request.FILES.get('image', None)
    
        try:
            share = get_object_or_404(CommunityPost, id=share_id, author=request.user)
            share.title = title
            share.description = description
            share.user_share_content = user_share_content
            if image:
                share.image = image
            share.save()
            
            messages.success(request, f'Knowledge Share "{title}" updated successfully!', extra_tags="shareKnowledgeEditSuccess")
        except Exception as e:
            messages.error(request, f'Error updating Knowledge Share: {str(e)}', extra_tags="shareKnowledgeEditError")
    
    return redirect('userShareKnowledge')

@user_only_required
def deleteShareKnowledge(request):
    if request.method == 'POST':
        share_id = request.POST.get('share_id')
        
        try:
            share = get_object_or_404(CommunityPost, id=share_id, author=request.user)
            share_title = share.title
            share.delete()
            
            messages.success(request, f'Knowledge Share "{share_title}" deleted successfully!', extra_tags="shareKnowledgeDeleteSuccess")
        except Exception as e:
            messages.error(request, f'Error deleting Knowledge Share: {str(e)}', extra_tags="shareKnowledgeDeleteError")
    
    return redirect('userShareKnowledge')


#----------------Ticket---------------------------------
@user_only_required
def userTickets(request):
    tickets = PurchaseTicket.objects.filter(user=request.user).select_related('event').order_by('-purchase_date')

    context = {
        'tickets':tickets
    }

    return render(request, "userDashboard/Dashboard/user_tickets.html", context)

#--------------------------Profile Section -----------------------------
@user_only_required
def profile(request):
    return render(request, "userProfile/profile.html")


@user_only_required
def userEditProfile(request):
    user = request.user

    if request.method == "POST":
        # Getting updated data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        land_address = request.POST.get('land_address')

        CustomUser = get_user_model()

        # Check username uniqueness
        if CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, "Username already exists.", extra_tags="userProfileUpdate")
            return redirect('edit-profile')

        # Check email uniqueness
        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, "Email already exists.", extra_tags="userProfileUpdate")
            return redirect('edit-profile')

        # Update user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.address = address
        user.land_address = land_address

        user.save()

        messages.success(request, "Your Profile Updated Successfully", extra_tags="userProfileUpdate")
        return redirect('profile')

    # GET request → show form
    return render(request, "userProfile/edit_profile.html", {"user": user})

@user_only_required
def userPasswordChange(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!', extra_tags="userProfileUpdate")
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.', extra_tags="userProfileUpdate")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userProfile/change_password.html', {
        'form': form
    })


@user_only_required
def cropTasks(request):
    user_crops = UserCropAdd.objects.filter(
        user=request.user,
        is_task_hidden=False
    ).select_related('crop').prefetch_related('crop__schedules')

    today = date.today()
    all_today_tasks = []
    crops_with_old_tasks = []

    for uc in user_crops:
        crop_old_tasks = []
        
        for schedule in uc.crop.schedules.all():
            task_date = uc.planted_date + timedelta(days=schedule.day_number)
            task_info = {
                'user_crop_id': uc.id,
                'crop_name': uc.crop.name,
                'task': schedule.task,
                'day_number': schedule.day_number,
                'task_date': task_date,
                'planted_date': uc.planted_date,  
            }
            
            if task_date == today:
                all_today_tasks.append(task_info)
            elif task_date < today:
                crop_old_tasks.append(task_info)
        
        if crop_old_tasks:
            crops_with_old_tasks.append({
                'user_crop_id': uc.id,
                'crop_name': uc.crop.name,
                'planted_date': uc.planted_date,
                'old_tasks': crop_old_tasks,
            })

    context = {
        'all_today_tasks': all_today_tasks,
        'crops_with_old_tasks': crops_with_old_tasks,
    }

    return render(request, "userDashboard/Dashboard/crop_tasks.html", context)


@user_only_required
def hideCrop(request, user_crop_id):
    if request.method == "POST":
        try:
            user_crop = UserCropAdd.objects.get(id=user_crop_id, user=request.user)
            user_crop.is_task_hidden = True
            user_crop.save()
            messages.success(request, "Crop task delete successfully.", extra_tags="deleteCropTask")
        except UserCropAdd.DoesNotExist:
            messages.error(request, "Crop not found.", extra_tags="deleteCropTask")
    return redirect("cropTasks")  # ← was "crop_tasks", must match url name exactly