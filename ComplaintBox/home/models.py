
# Create your models here.
from django.db import models
from django.utils import timezone
from django.urls import reverse
from user.models import UserProfile , WorkerProfile
#from django.contrib.postgres.fields import ArrayField

class TaskHistory(models.Model):
     title = models.CharField(max_length=100)
     complaint = models.TextField() #unrestricted text
     date_posted=models.DateTimeField(default=timezone.now)#(auto_now=True)#updated date post everytime post is updated
     #auto_now_add only when date is created
     #default
     assignedby = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  #IF USER IS DELETED POSTS ARE DELETED
     assigned=models.ForeignKey(WorkerProfile,on_delete=models.CASCADE,null =True,default=None)  
     profession=models.CharField(max_length=100)
     status=models.CharField(default = "PENDING", max_length = 50)
    #  Comments=ArrayField(
    #      models.TextField(blank=True,default = None))
     
     Comments = models.TextField(blank=True,default = None)
     def get_absolute_url(self):
        return reverse('detailed_task', kwargs={'pk':self.pk})
     def __str__(self):
         #return self.title4es
         return self.title
class Comment(models.Model):
	complaint=models.ForeignKey(TaskHistory,on_delete=models.CASCADE,related_name='comments')
	user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	content=models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'comment on {} by {}'.format(self.post.title,self.user.username)