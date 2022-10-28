from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth.models import User


#django form for user registration:


class Createuserform(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = [
            'username','email', 'role', 'image', 'phone_no', 'address', 'preference', 'profession', 'biodata', 'password1'
        ]

'''
created all the fields in one form along with optional ones
will hide them using html
'''