from django.db import models
#model containing user's data
class User(models.Model):
    Name : models.CharField(max_length=100)
    Username : models.CharField(max_length=100)
    Address : models.TextField(default = None)
    Phone_no : models.PositiveBigIntegerField()
    Email : models.EmailField()
    #Password :
    #Star :
    #Preference :

"""
have to add default values. 
will complete the model after adding default values
"""
