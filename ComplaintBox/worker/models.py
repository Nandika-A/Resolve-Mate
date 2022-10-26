from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.core.validators import MaxValueValidator
from .manager import *
from django.contrib.auth.models import User
#model containing worker's data
class WorkerProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    
    Bio : models.TextField(default = None)
    Phone_no : models.PositiveBigIntegerField(default = None)
    Star : ArrayField(
            models.DecimalField(blank=True,validators=[
                                       MaxValueValidator(5)]),
            size=2,
        )
    Profession : models.CharField(max_length=100)
    
    