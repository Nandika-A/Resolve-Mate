from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#django form for user registration:
class UserRegistrationForm(UserCreationForm):
    #additional fields to be included in inbuilt user registration form in addition to username and password
    email = forms.EmailField()
    Name = forms.CharField()
    Address = forms.TextField()
    Phone_no = forms.PositiveBigIntegerField()
    Star = forms.PositiveSmallIntegerField() #max 5 stars(all integers)
    Preference = forms.JSONField() #dictionary field
    class Meta:
        model = User #form is saved in user model
        # the order in which the fields in the form are to be displayed:
        fields = [
            'username', 'address', 'phonenumber', 'email', 'star', 'prefernces', 'password1', 'password2'
        ]