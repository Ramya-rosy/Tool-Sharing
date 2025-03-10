from django.db import models

from users.models import User
from listings.models import Listing


# Create your models here.
status_options = (
    ('requested', 'requested'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
    ('returned', 'returned'),
    ('return_confirmed', 'return_confirmed')
)


class Borrowing(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lender')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrower')
    borrowing_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=status_options, default=status_options[0][0])
