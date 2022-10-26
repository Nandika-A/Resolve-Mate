from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from .manager import *
#model containing worker's data
class WorkerProfile(AbstractUser):
    username : None
    Name : models.CharField(max_length=100)
    Bio : models.TextField(default = None)
    Phone_no : models.PositiveBigIntegerField(default = None)
    Email : models.EmailField(unique=True)
    Password = models.CharField(max_length=50, default=None)
    #to store present rating and number of users who have rated in a list.
    #to access the values in the list use Star__0 and Star__1
    Star : ArrayField(
            models.IntegerField(blank=True),
            size=2,
        )
    Profession : models.CharField(max_length=100)
    USERNAME_FIELD = 'Name'
    