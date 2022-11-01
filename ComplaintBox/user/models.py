
from email.policy import default
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField
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
    #both user and worker data can be accessed using one table, just by defining roles
    class Role(models.TextChoices):
        USER = "USER", "User"
        WORKER = "WORKER", "Worker"
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    #username = models.CharField(max_length = 200, default = None)
    #email = models.EmailField(max_length=200, help_text='Required')
    base_role = Role.USER
    role = models.CharField(max_length=50, choices = Role.choices)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')  #images will get saved in directory called profile_pics
    
    Star= models.JSONField(
        models.DecimalField(blank=True, validators=[
            MaxValueValidator(5)], decimal_places = 2, max_digits = 3),
        default = []
    )
    
    phone_no= models.CharField(default=None,max_length=50)
    
    Star= models.JSONField(default=dict)

    
    
    
    phone_no= models.CharField(default=None,max_length=50)

    address = models.TextField(default = None)
    preference= ArrayField(
        models.DecimalField(blank=True, validators=[
            MaxValueValidator(5)], decimal_places = 2, max_digits = 3),
        size=2,default = None
    )

    USERNAME_FIELD = 'user'
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.username} Profile'  #will dispaly in a nice way otherwise will return object name
class WorkerProfile(models.Model):
    workername=models.ForeignKey(UserProfile,on_delete=models.CASCADE)  
    profession = models.CharField(max_length=100, default=None)
    biodata = models.TextField(default = None)
    Star= models.JSONField(default=dict)
    
'''    
class Usermanager(models.Manager): #to separate user and worker data.
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = UserProfile.Role.USER) 
    
class UserData(UserProfile):
    objects = Usermanager()
    base_role = UserProfile.Role.USER
    class Meta:
        proxy = True #won't create a new table for user
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = UserProfile.Role.USER
        return super().save(*args, **kwargs)
    @property #to access additional fields in user model
    def more(self):
        return Usermore.objects.filter(user_id=self.id)
    
class Usermore(models.Model):
    user=models.OneToOneField(UserProfile,on_delete=models.CASCADE,null=True)
    address = models.TextField(default = None)
    preference= models.JSONField(null=True, default=dict)
    USERNAME_FIELD = 'user'
     
class Workermanager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = UserProfile.Role.WORKER) 
    
class WorkerData(UserProfile):
    objects = Workermanager()
    base_role = UserProfile.Role.WORKER
    class Meta:
        proxy = True
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = UserProfile.Role.USER
        return super().save(*args, **kwargs)
    @property
    def more(self):
        return Workermore.objects.filter(user_id=self.id)
    
class Workermore(models.Model):
    user=models.OneToOneField(UserProfile,on_delete=models.CASCADE,null=True)
    biodata = models.TextField(default = None)
    profession = models.CharField(max_length=100, default=None)
   ''' 