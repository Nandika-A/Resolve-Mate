from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, WorkerProfile
from django.contrib.auth.models import User


#django form for user registration:


class Createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username','email','password1', 'password2'
        ]
class AddDetails(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = [
            'image', 'phone_no', 'address',
        ]
class AddWorkerDetails(UserCreationForm):
    class Meta:
        model=WorkerProfile
        fields=[
            'profession', 'biodata',
        ]

'''
created all the fields in one form along with optional ones
will hide them using html
'''