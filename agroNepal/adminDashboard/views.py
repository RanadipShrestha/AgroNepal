from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.models import CustomUser
from agro.models import Crop, CropSchedule, Contact, Event, Blog, CropExpense, CropSale, UserCropAdd, CommunityPost
from payment.models import PurchaseTicket
from .decorators import admin_only_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import timedelta
from django.db.models import Count, Sum
# Create your views here.

@admin_only_required
def adminDashboard(request):
    total_users = CustomUser.objects.count()
    total_crops = Crop.objects.count()
    total_posts = CommunityPost.objects.count()
    total_contacts = Contact.objects.count()
    total_events = Event.objects.count()
    total_blogs = Blog.objects.count()

    # User Growth Data (Last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    user_growth = CustomUser.objects.filter(date_joined__gte=six_months_ago) \
        .annotate(month=TruncMonth('date_joined')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')

    user_growth_labels = [item['month'].strftime('%b %Y') for item in user_growth]
    user_growth_data = [item['count'] for item in user_growth]

    # Top Planted Crops Data
    top_crops = UserCropAdd.objects.values('crop__name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:7]
    
    top_crops_labels = [item['crop__name'] for item in top_crops]
    top_crops_data = [item['count'] for item in top_crops]

    # Top 10 Active Farmers (by total crops planted)
    top_users = UserCropAdd.objects.values('user__username', 'user__first_name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:10]
    
    top_users_labels = [item['user__first_name'] or item['user__username'] for item in top_users]
    top_users_data = [item['count'] for item in top_users]

    # Top 10 Ticket Buyers
    ticket_buyers = PurchaseTicket.objects.values('user__username', 'user__first_name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:10]
    
    ticket_buyers_labels = [item['user__first_name'] or item['user__username'] for item in ticket_buyers]
    ticket_buyers_data = [item['count'] for item in ticket_buyers]

    # Financial Data
    total_sales = CropSale.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = CropExpense.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_users': total_users,
        'total_crops': total_crops,
        'total_posts': total_posts,
        'total_contacts': total_contacts,
        'total_events': total_events,
        'user_growth_labels': user_growth_labels,
        'user_growth_data': user_growth_data,
        'top_crops_labels': top_crops_labels,
        'top_crops_data': top_crops_data,
        'top_users_labels': top_users_labels,
        'top_users_data': top_users_data,
        'ticket_buyers_labels': ticket_buyers_labels,
        'ticket_buyers_data': ticket_buyers_data,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
    }
    return render(request, 'adminDashboard/dashboard/dashboard.html', context)


@admin_only_required
def adminUsers(request):
  query = request.GET.get('q', '')
  if query:
      users_list = CustomUser.objects.filter(
          Q(username__icontains=query) | Q(email__icontains=query) | 
          Q(first_name__icontains=query) | Q(last_name__icontains=query)
      ).order_by('-date_joined')
  else:
      users_list = CustomUser.objects.all().order_by('-date_joined')
  paginator = Paginator(users_list, 10)
  page_number = request.GET.get('page')
  users = paginator.get_page(page_number)
  return render(request, 'adminDashboard/dashboard/user/users.html', {'users': users, 'search_query': query}) 

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
            messages.error(request, "Required fields missing!", extra_tags="adminUserAddError")
            return redirect('adminAddUser')

        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.", extra_tags="adminUserAddError")
            return redirect('adminAddUser')

        # Check for duplicate username
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken.", extra_tags="adminUserAddError")
            return redirect('adminAddUser')

        # Check for duplicate email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"Email '{email}' is already registered.", extra_tags="adminUserAddError")
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

            messages.success(request, f"User '{username}' created successfully.", extra_tags="adminUser")
            return redirect('adminUsers')

        except Exception as e:
            messages.error(request, "There is an error while creating user.", extra_tags="adminUserAddError")

    return render(request, 'adminDashboard/dashboard/user/add_user.html')

@admin_only_required
def adminEditUser(request, user_id):
    edit_user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        land_address = request.POST.get('land_address', '')
        is_staff = request.POST.get('is_staff') == 'true'
        is_active = request.POST.get('is_active') == 'true'

        # Update object in memory for form display in case of error
        edit_user.first_name = first_name
        edit_user.last_name = last_name
        edit_user.username = username
        edit_user.email = email
        edit_user.phone_number = phone_number
        edit_user.address = address
        edit_user.land_address = land_address
        edit_user.is_staff = is_staff
        edit_user.is_active = is_active

        # Check for duplicate username (excluding current user)
        if CustomUser.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, f"Username '{username}' is already taken.", extra_tags="adminUserEditError")
            return render(request, 'adminDashboard/dashboard/user/edit_user.html', {'edit_user': edit_user})

        # Check for duplicate email (excluding current user)
        if CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, f"Email '{email}' is already registered.", extra_tags="adminUserEditError")
            return render(request, 'adminDashboard/dashboard/user/edit_user.html', {'edit_user': edit_user})
        
        try:
            edit_user.save()
            messages.success(request, f"User '{edit_user.username}' updated successfully.", extra_tags="adminUser")
            return redirect('adminUsers')
        except Exception as e:
            messages.error(request, f"Error updating user: {str(e)}", extra_tags="adminUserEditError")
            
    return render(request, 'adminDashboard/dashboard/user/edit_user.html', {'edit_user': edit_user})

@admin_only_required
def adminDeleteUser(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_to_delete = get_object_or_404(CustomUser, id=user_id)
        if user_to_delete == request.user:
            messages.error(request, "You cannot delete yourself", extra_tags="adminUser")
        else:
            username = user_to_delete.username
            user_to_delete.delete()
            messages.success(request,"user deleted successfully", extra_tags="adminUser")
    return redirect('adminUsers')

@admin_only_required
def adminCrops(request):
    query = request.GET.get('q', '')
    if query:
        crops_list = Crop.objects.prefetch_related('schedules').filter(
            Q(name__icontains=query)
        ).order_by('-id')
    else:
        crops_list = Crop.objects.prefetch_related('schedules').all().order_by('-id')
    paginator = Paginator(crops_list, 10)
    page_number = request.GET.get('page')
    crops = paginator.get_page(page_number)
    return render(request, 'adminDashboard/dashboard/crop/crops.html', {'crops': crops, 'search_query': query})

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

        messages.success(request, f"Crop '{name}' updated successfully.", extra_tags="admincrop")

    return redirect('adminCrops')

@admin_only_required
def adminDeleteCrop(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        crop = get_object_or_404(Crop, id=crop_id)
        crop_name = crop.name
        crop.delete()
        messages.success(request, "Crop deleted successfully.",  extra_tags="admincrop")
    return redirect('adminCrops')

@admin_only_required
def adminContacts(request):
    query = request.GET.get('q', '')
    if query:
        contacts_list = Contact.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(subject__icontains=query)
        ).order_by('-id')
    else:
        contacts_list = Contact.objects.all().order_by('-id')
        
    paginator = Paginator(contacts_list, 10)
    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)
    context = {
        'contacts': contacts,
        'search_query': query
    }
    return render(request, 'adminDashboard/dashboard/contact/contacts.html', context)

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
    today = timezone.now().date()
    query = request.GET.get('q', '')
    
    upcoming_list = Event.objects.filter(date__gte=today)
    past_list = Event.objects.filter(date__lt=today)
    
    if query:
        upcoming_list = upcoming_list.filter(Q(name__icontains=query) | Q(location__icontains=query))
        past_list = past_list.filter(Q(name__icontains=query) | Q(location__icontains=query))
    
    upcoming_list = upcoming_list.order_by('date')
    past_list = past_list.order_by('-date')
    
    # Upcoming events pagination
    up_paginator = Paginator(upcoming_list, 10)
    up_page = request.GET.get('up_page')
    upcoming_events = up_paginator.get_page(up_page)
    
    # Past events pagination
    past_paginator = Paginator(past_list, 10)
    past_page = request.GET.get('past_page')
    past_events = past_paginator.get_page(past_page)
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'search_query': query,
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
                author=request.user,
            )
            messages.success(request, "New Event Added Successfully", extra_tags="adminEvent")
            return redirect('adminEvents')

        except:
            messages.error(request, 'There is issues in the enter data please correct that', extra_tags="adminEvent")
    return render(request, 'adminDashboard/dashboard/event/add_event.html')

@admin_only_required
def adminEditEvent(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.name = request.POST.get('name')
        if 'image' in request.FILES:
            event.image = request.FILES.get('image')
        event.price = request.POST.get('price')
        event.description = request.POST.get('description')
        event.location = request.POST.get('location')
        event.date = request.POST.get('date')
        event.eventStartTime = request.POST.get('eventStartTime')
        event.event_duration = request.POST.get('event_duration')
        event.guest = request.POST.get('guest')
        
        old_total = event.total_ticket
        new_total = int(request.POST.get('total_ticket'))
        diff = new_total - old_total
        event.total_ticket = new_total
        event.available_ticket = max(0, event.available_ticket + diff)
        
        try:
            event.save()
            messages.success(request, f"Event '{event.name}' updated successfully.", extra_tags="adminEvent")
            return redirect('adminEvents')
        except Exception as e:
            messages.error(request, "There is an error while updateding Event. Please Try Again.", extra_tags="adminEvent")
            
    return render(request, 'adminDashboard/dashboard/event/edit_event.html', {'event': event})

@admin_only_required
def adminDeleteEvent(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        event_name = event.name
        event.delete()
        messages.success(request, f"Event '{event_name}' deleted successfully", extra_tags="adminEvent")
    return redirect('adminEvents')


#-------------------Blog Management------------

@admin_only_required
def adminBlogs(request):
    query = request.GET.get('q', '')
    if query:
        blogs_list = Blog.objects.filter(
            Q(title__icontains=query) | Q(author__username__icontains=query)
        ).order_by('-create_date')
    else:
        blogs_list = Blog.objects.all().order_by('-create_date')
    paginator = Paginator(blogs_list, 10)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    context = {
        'blogs': blogs,
        'search_query': query,
    }
    return render(request, 'adminDashboard/dashboard/blog/blogs.html', context)

@admin_only_required
def adminAddBlog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        blog_content = request.POST.get('blog_content', '')
        image = request.FILES.get('image')
        
        try:
            Blog.objects.create(
                title=title,
                description=description,
                blog_content=blog_content,
                image=image,
                author=request.user
            )
            messages.success(request, "Blog added successfully.", extra_tags="adminBlog")
            return redirect('adminBlogs')
        except Exception:
            messages.error(request, "Error adding blog.", extra_tags="adminBlog")
            
    return render(request, 'adminDashboard/dashboard/blog/add_blog.html')

@admin_only_required
def adminEditBlog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.description = request.POST.get('description')
        blog.blog_content = request.POST.get('blog_content', '')
        
        if 'image' in request.FILES:
            blog.image = request.FILES.get('image')
            
        try:
            blog.save()
            messages.success(request, "Blog updated successfully.", extra_tags="adminBlog")
            return redirect('adminBlogs')
        except Exception as e:
            messages.error(request, "Error updating blog.", extra_tags="adminBlog")
    context = {
        'blog': blog
    }       
    return render(request, 'adminDashboard/dashboard/blog/edit_blog.html', context)

@admin_only_required
def adminDeleteBlog(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)
        blog_title = blog.title
        blog.delete()
        messages.success(request, "Blog deleted successfully.", extra_tags="adminBlog")
    return redirect('adminBlogs')

@admin_only_required
def adminTickets(request):
    query = request.GET.get('q', '')
    if query:
        tickets_list = PurchaseTicket.objects.filter(
            Q(user__username__icontains=query) | Q(event__name__icontains=query)
        ).order_by('-purchase_date')
    else:
        tickets_list = PurchaseTicket.objects.all().order_by('-purchase_date')
        
    paginator = Paginator(tickets_list, 10)
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)
    
    context = {
        'tickets': tickets,
        'search_query': query
    }
    return render(request, 'adminDashboard/dashboard/ticket/tickets.html', context)


@admin_only_required
def adminUserExpenses(request):
    query = request.GET.get('q', '')
    if query:
        expenses_list = CropExpense.objects.filter(user_crop__user__username__icontains=query).order_by('-spend_date')
    else:
        expenses_list = CropExpense.objects.all().order_by('-spend_date')
        
    paginator = Paginator(expenses_list, 10)
    page_number = request.GET.get('page')
    expenses = paginator.get_page(page_number)
    
    context = {
        'expenses': expenses,
        'search_query': query
    }
    return render(request, 'adminDashboard/dashboard/expenseAndSale/user_expenses.html', context)

@admin_only_required
def adminEditUserExpense(request, expense_id):
    expense = get_object_or_404(CropExpense, id=expense_id)
    if request.method == 'POST':
        expense.amount = request.POST.get('amount')
        expense.spend_date = request.POST.get('spend_date')
        expense.note = request.POST.get('note', '')
        
        try:
            expense.save()
            messages.success(request, "Expense record updated successfully.", extra_tags="adminUserExpense")
            return redirect('adminUserExpenses')
        except Exception as e:
            messages.error(request, "Error updating expense record.", extra_tags="adminUserExpense")
            
    context = {'expense': expense}
    return render(request, 'adminDashboard/dashboard/expenseAndSale/edit_user_expense.html', context)

@admin_only_required
def adminDeleteUserExpense(request):
    if request.method == 'POST':
        expense_id = request.POST.get('expense_id')
        expense = get_object_or_404(CropExpense, id=expense_id)
        expense.delete()
        messages.success(request, "Expense record deleted successfully.", extra_tags="adminUserExpense")
    return redirect('adminUserExpenses')

@admin_only_required
def adminUserSales(request):
    query = request.GET.get('q', '')
    if query:
        sales_list = CropSale.objects.filter(user_crop__user__username__icontains=query).order_by('-sale_date')
    else:
        sales_list = CropSale.objects.all().order_by('-sale_date')
        
    paginator = Paginator(sales_list, 10)
    page_number = request.GET.get('page')
    sales = paginator.get_page(page_number)
    
    context = {
        'sales': sales,
        'search_query': query
    }
    return render(request, 'adminDashboard/dashboard/expenseAndSale/user_sales.html', context)

@admin_only_required
def adminEditUserSale(request, sale_id):
    sale = get_object_or_404(CropSale, id=sale_id)
    if request.method == 'POST':
        sale.amount = request.POST.get('amount')
        sale.quantity = request.POST.get('quantity') or None
        sale.sale_date = request.POST.get('sale_date')
        sale.buyer_name = request.POST.get('buyer_name', '')
        sale.note = request.POST.get('note', '')
        
        try:
            sale.save()
            messages.success(request, "Sale record updated successfully.", extra_tags="adminUserSale")
            return redirect('adminUserSales')
        except Exception as e:
            messages.error(request, "Error updating sale record.", extra_tags="adminUserSale")
            
    context = {'sale': sale}
    return render(request, 'adminDashboard/dashboard/expenseAndSale/edit_user_sale.html', context)

@admin_only_required
def adminDeleteUserSale(request):
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        sale = get_object_or_404(CropSale, id=sale_id)
        sale.delete()
        messages.success(request, "Sale record deleted successfully.", extra_tags="adminUserSale")
    return redirect('adminUserSales')

@admin_only_required
def adminUserPlantedCrops(request):
    query = request.GET.get('q', '')
    if query:
        user_crops_list = UserCropAdd.objects.filter(
            Q(user__username__icontains=query) | Q(crop__name__icontains=query)
        ).order_by('-planted_date')
    else:
        user_crops_list = UserCropAdd.objects.all().order_by('-planted_date')
        
    paginator = Paginator(user_crops_list, 10)
    page_number = request.GET.get('page')
    user_crops = paginator.get_page(page_number)
    
    context = {
        'user_crops': user_crops,
        'search_query': query
    }
    return render(request, 'adminDashboard/dashboard/crop/user_planted_crops.html', context)

@admin_only_required
def adminEditUserPlantedCrop(request, crop_id):
    user_crop = get_object_or_404(UserCropAdd, id=crop_id)
    if request.method == 'POST':
        user_crop.planted_date = request.POST.get('planted_date')
        user_crop.notes = request.POST.get('notes', '')
        user_crop.is_task_hidden = request.POST.get('is_task_hidden') == 'on'
        
        crop_id_new = request.POST.get('crop_id')
        if crop_id_new:
            user_crop.crop_id = crop_id_new
            
        try:
            user_crop.save()
            messages.success(request, "Planted crop record updated successfully.", extra_tags="adminUserCrop")
            return redirect('adminUserPlantedCrops')
        except Exception as e:
            messages.error(request, "Error updating planted crop record.", extra_tags="adminUserCrop")
            
    crops = Crop.objects.all()
    context = {'user_crop': user_crop, 'crops': crops}
    return render(request, 'adminDashboard/dashboard/crop/edit_user_planted_crop.html', context)

@admin_only_required
def adminDeleteUserPlantedCrop(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        user_crop = get_object_or_404(UserCropAdd, id=crop_id)
        user_crop.delete()
        messages.success(request, "Planted crop record deleted successfully.", extra_tags="adminUserCrop")
    return redirect('adminUserPlantedCrops')

#------------Community post ----------------
@admin_only_required
def adminCommunityPosts(request):
    query = request.GET.get('q', '')
    if query:
        posts_list = CommunityPost.objects.filter(
            Q(title__icontains=query) | Q(author__username__icontains=query)
        ).order_by('-create_date')
    else:
        posts_list = CommunityPost.objects.all().order_by('-create_date')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'search_query': query,
    }
    return render(request, 'adminDashboard/dashboard/communityPost/community_posts.html', context)

@admin_only_required
def adminAddCommunityPost(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_share_content = request.POST.get('user_share_content', '')
        image = request.FILES.get('image')
        
        try:
            CommunityPost.objects.create(
                title=title,
                description=description,
                user_share_content=user_share_content,
                image=image,
                author=request.user
            )
            messages.success(request, "Community post added successfully.", extra_tags="adminCommunityPost")
            return redirect('adminCommunityPosts')
        except Exception:
            messages.error(request, "Error adding post", extra_tags="adminCommunityPost")
    return render(request, 'adminDashboard/dashboard/communityPost/add_community_post.html')

@admin_only_required
def adminEditCommunityPost(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')
        post.user_share_content = request.POST.get('user_share_content', '')
        
        if 'image' in request.FILES:
            post.image = request.FILES.get('image')
            
        try:
            post.save()
            messages.success(request, "Community post updated successfully.", extra_tags="adminCommunityPost")
            return redirect('adminCommunityPosts')
        except Exception as e:
            messages.error(request, "Error updating post", extra_tags="adminCommunityPost")
    context ={
        'post': post
    }
    return render(request, 'adminDashboard/dashboard/communityPost/edit_community_post.html', context)

@admin_only_required
def adminDeleteCommunityPost(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(CommunityPost, id=post_id)
        post_title = post.title
        post.delete()
        messages.success(request, "Post deleted successfully.", extra_tags="adminCommunityPost")
    return redirect('adminCommunityPosts')