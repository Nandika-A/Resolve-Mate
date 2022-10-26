from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from .manager import *




class CustomAccountManager(BaseUserManager):
    def create_user(self,Email,Name,Password,**other_fields):
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_superuser',True)
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        return self.create_user(Email,Name,Password,**other_fields)

    def create_user(self,Email,Name,Password,**other_fields):
        if not Email:
            raise ValueError('You must provide an email address')
    
        email=self.normalize_email(email)
        user=self.model(Email=Email,Name=Name,**other_fields)
        user.set_password(Password)
        user.save
        return user

#model containing user's data
class UserProfile(AbstractBaseUser,PermissionsMixin):
    #username :models.CharField(max_length=100)
    Email : models.CharField(unique=True,max_length=99)
    Name : models.CharField(max_length=100)
    Address : models.TextField(default = None)
    Phone_no : models.PositiveBigIntegerField(default = None)
    Password = models.CharField(max_length=50, default=None)
    Star : ArrayField(
            models.DecimalField(blank=True,validators=[
                                       MaxValueValidator(5)]),
            size=2,
        )
    is_active:models.BooleanField(default=False)
    Preference : models.JSONField(null=True, default=dict)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
         return self.Email