from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Borrowing
from listings.models import Listing
from users.models import User


# Create your views here.
@login_required(login_url='login')
def item_request(request, item_id):
    # get user
    user = request.user
    # get item
    item = Listing.objects.get(pk=item_id)
    if item.availability:
        # get owner
        owner = item.user
        # create borrow
        borrowing = Borrowing()
        borrowing.lender = owner
        borrowing.borrower = user
        borrowing.listing = item
        borrowing.due_date = timezone.now()
        borrowing.save()

        messages.success(request, 'Borrow Request sent successfully!',extra_tags='borrow')
    else:
        messages.error(request, 'Item is not available!',extra_tags='borrow')

    return redirect('profile')


@login_required(login_url='login')
def item_request_approve(request, borrow_id):
    # get user
    user = request.user
    # get borrow
    borrowing = Borrowing.objects.get(pk=borrow_id)
    # update item
    item = borrowing.listing
    item.availability = False
    duration = item.borrow_duration
    item.save()
    # update borrow
    borrowing.due_date = datetime.now() + timedelta(days=duration)
    borrowing.status = 'accepted'
    borrowing.save()
    messages.success(request, 'Borrow Request was approved successfully!',extra_tags='approval')
    return redirect('profile')


@login_required(login_url='login')
def item_request_reject(request, borrow_id):
    # get user
    user = request.user
    # get borrow
    borrowing = Borrowing.objects.get(pk=borrow_id)
    borrowing.status = 'rejected'
    borrowing.save()
    messages.success(request, 'Borrow Request was rejected successfully!',extra_tags='approval')
    return redirect('profile')


@login_required(login_url='login')
def item_request_cancel(request, borrow_id):
    # get user
    user = request.user
    # get borrow
    borrowing = Borrowing.objects.get(pk=borrow_id)#.filter(status='requested')
    borrowing.delete()
    messages.success(request, 'Borrow Request was deleted successfully!',extra_tags='borrow')
    return redirect('profile')


@login_required(login_url='login')
def item_return(request, borrow_id):
    # get user
    user = request.user
    # get borrow
    borrowing = Borrowing.objects.get(pk=borrow_id)#.filter(status='accepted')
    borrowing.status = 'returned'
    borrowing.save()
    messages.success(request, 'Borrow Return was sent successfully!',extra_tags='borrow')
    return redirect('profile')


@login_required(login_url='login')
def item_return_confirm(request, borrow_id):
    # get user
    user = request.user
    # get borrow
    borrowing = Borrowing.objects.get(pk=borrow_id)
    # update item
    item = borrowing.listing
    item.availability = True
    item.save()
    # update borrow
    borrowing.status = 'return_confirmed'
    borrowing.save()

    messages.success(request, 'Item Return was confirmed successfully!',extra_tags='approval')
    return redirect('profile')


@login_required(login_url='login')
def item_return_override(request, borrow_id):
    # get user
    user = request.user
    # get borrow
    borrowing = Borrowing.objects.get(pk=borrow_id)
    # update item
    item = borrowing.listing
    item.availability = True
    item.save()
    # update borrow
    borrowing.status = 'return_confirmed'
    borrowing.save()

    messages.success(request, 'Item Return was confirmed successfully!',extra_tags='approval')
    return redirect('profile')
