from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

from .forms import listingForm
from .models import Listing
from borrowing.models import Borrowing


@login_required(login_url='login')
def search(request):
    user = request.user
    query = request.GET.get('q','').strip()
    availability = request.GET.get('availability')
    category = request.GET.get('category')
    
    devices = Listing.objects.filter(~Q(user=user))

    if query:
        devices = devices.filter(
            # Q(name__iexact=query) | 
            Q(name__icontains=query) |
            # Q(category__iexact=query) | 
            # Q(category__icontains=query) |
            # Q(location__iexact=query) | 
            Q(location__icontains=query)
        )
 
    # else:
    #     return redirect('listings')
    
    if availability:
        if availability == 'available':
            devices = devices.filter(availability=True)
        elif availability == 'unavailable':
            devices = devices.filter(availability=False)

    if category:
        devices = devices.filter(
            Q(category__iexact=category) | 
            Q(category__icontains=category)
        )
    
    no_results = query and not devices.exists()
   
    return render(request, 'listings/listings.html', {'devices': devices,'no_results': no_results})


@login_required(login_url='login')
def post_item(request):
    user = request.user
    context = {}

    if request.method == 'GET':
        form = listingForm()
        context['form'] = form

    if request.method == 'POST':
        form = listingForm(request.POST, request.FILES)
        if form.is_valid:
            print(form.errors)
            listing = form.save(commit=False)
            listing.user = user
            if not listing.email or listing.email == "":
                listing.email = user.university_email
            listing.save()

            return redirect('profile')
        else:
            print(form.errors)

    return render(request, 'listings/post_item.html', context=context)


@login_required(login_url='login')
def my_listings(request):
    context = {}
    user = request.user
    listings = Listing.objects.filter(user=user)

    context['listings'] = listings
    context['owner'] = True
    return render(request, 'listings/listings.html', context=context)


@login_required(login_url='login')
def listings(request):
    context = {}
    user = request.user
    listings = Listing.objects.filter(~Q(user=user))
    borrowings = Borrowing.objects.filter(borrower=user).exclude(status='return_confirmed').exclude(status='rejected')
    lendings = Borrowing.objects.filter(lender=user)

    context['listings'] = listings
    context['borrowings'] = list(map(lambda x: x.listing_id, borrowings))
    context['lendings'] = list(lendings)
    context['owner'] = False
    return render(request, 'listings/listings.html', context=context)


@login_required(login_url='login')
def item_detail(request, item_id):
    context = {}
    # get item
    item = Listing.objects.get(pk=item_id)
    context['item'] = item

    # Assuming the Listing model has a field 'owner' which is a ForeignKey to User
    owner = item.user
    context['owner'] = owner
    
    # get form
    form = listingForm(instance=item)
    context['form'] = form
    return render(request, 'listings/item_detail.html', context=context)


@login_required(login_url='login')
def item_edit(request, item_id):
    user = request.user
    context = {}
    # get item
    item = Listing.objects.get(pk=item_id)
    context['item'] = item
    # get form
    form = listingForm(instance=item)
    context['form'] = form

    if request.method == 'POST':
        form = listingForm(request.POST, request.FILES, instance=item)
        if form.is_valid:
            form.save()
            return redirect('profile')

    return render(request, 'listings/item_edit.html', context=context)


@login_required(login_url='login')
def item_delete(request, item_id):
    user = request.user
    context = {}
    # get item
    item = Listing.objects.get(pk=item_id)
    # delete image
    item.image.delete(save=True)
    # delete item
    item.delete()
    # send message
    messages.success(request, 'Item Deleted successfully.',extra_tags='posted')

    return redirect('profile')


@login_required(login_url='login')
def bridge_page(request):
    return render(request, 'listings/bridge_page.html')
