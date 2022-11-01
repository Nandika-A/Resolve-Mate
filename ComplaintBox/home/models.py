
# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from user.models import UserProfile , WorkerProfile
from django.contrib.postgres.fields import ArrayField

class TaskHistory(models.Model):
     title = models.CharField(max_length=100)
     complaint = models.TextField() #unrestricted text
     date_posted=models.DateTimeField(default=timezone.now)#(auto_now=True)#updated date post everytime post is updated
     #auto_now_add only when date is created
     #default
     assignedby = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  #IF USER IS DELETED POSTS ARE DELETED
     assigned=models.ForeignKey(WorkerProfile,on_delete=models.CASCADE)  
     profession=models.CharField(max_length=100)
     status=models.CharField(default = "PENDING", max_length = 50)
     Comments=ArrayField(
         models.TextField(blank=True,default = None))
     def __str__(self):
         return self.title4es
