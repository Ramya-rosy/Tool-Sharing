# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime, timezone

from users.models import User


CATEGORY_OPTIONS = (('mechanic', 'Mechanical Engineering'), ('chemical', 'Chemical Engineering'), ('electrical', 'Electrical Engineering'))

#Create your models here.
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    category = models.CharField(max_length=10, choices=CATEGORY_OPTIONS)
    location = models.TextField()
    availability = models.BooleanField(default=True,blank=True)
    # availability_date = models.DateTimeField(default=timezone.now)
    borrow_duration = models.PositiveIntegerField(default=1, blank=False, validators=[MinValueValidator(1)])
    email = models.EmailField(null=False, blank=True)
    comments = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=True)
    image = models.ImageField(upload_to='images/')