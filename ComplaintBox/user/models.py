from django.db import models
from django.contrib.auth.models import User


from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
#from .manager import *



#after making changes to models we have to make migration
#after this go to users admin.py and register models
# class Profile(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     image=models.ImageField(default='default.jpg',upload_to='profile_pics')  #images will get saved in directory called profile_pics
#
#     def __str__(self):
#         return f'{self.user.username} Profile'  #will dispaly in a nice way otherwise will return object name



# model containing user's data
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')  #images will get saved in directory called profile_pics
    Star: ArrayField(
        models.DecimalField(blank=True, validators=[
            MaxValueValidator(5)]),
        size=2,
    )
    Address: models.TextField(default=None)
    Phone_no: models.PositiveBigIntegerField(default=None)
    Preference: models.JSONField(null=True, default=dict)
    def __str__(self):
        return f'{self.user.username} Profile'  #will dispaly in a nice way otherwise will return object name
    