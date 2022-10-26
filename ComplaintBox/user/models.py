from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.operations import HStoreExtension
#model containing user's data
class User(models.Model):
    Name : models.CharField(max_length=100)
    Username : models.CharField(max_length=100).foreignkey
    Address : models.TextField(default = None)
    Phone_no : models.PositiveBigIntegerField()
    Email : models.EmailField()
    Password : models.CharField(max_length=100)

    Star : ArrayField(models.DecimalField(decimal_places=2),models.IntegerField())    
    #Preference :

#workers table
#A person can login as an user and additionally sign up for a worker 
#Only additional data is saved in this table
class Workers(models.Model):
    Bio=models.TextField()
    Star : ArrayField(models.DecimalField(decimal_places=2),models.IntegerField())    
    UPI_Id:models.CharField(maxlength=100)
    Profession : models.CharField(max_length=100)
    Star : ArrayField(models.DecimalField(decimal_places=2),models.IntegerField())

class task_history(models.Model):
    complainee=models.ForeignKey(User)
    Profession=models.CharField(max_length=100)
    Complaint=models.TextField()
    Status=models.CharField(max_length=100)
    image=models.ImageField(upload_to='/images')
    fixer=models.ForeignKey(Workers,default=None)
    comments=ArrayField(models.TextField())

#comments use textfield
"""
have to add default values. 
will complete the model after adding default values
"""
