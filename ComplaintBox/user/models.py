from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from .manager import *
#model containing user's data
class UserProfile(AbstractUser):
    username :None
    Email : models.EmailField(unique=True)
    Name : models.CharField(max_length=100)
    Address : models.TextField(default = None)
    Phone_no : models.PositiveBigIntegerField(default = None)
    Password = models.CharField(max_length=50, default=None)
    Star : models.PositiveSmallIntegerField(null=True, blank=True, validators=[
                                       MaxValueValidator(5)])
    Preference : models.JSONField(null=True, default=dict)
    
    USERNAME_FIELD = 'Email'
    