from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

#django form for user registration:
class UserRegistrationForm(UserCreationForm):
    #additional fields to be included in inbuilt user registration form in addition to username and password
    
    Name = forms.CharField()
    Email = forms.EmailField()
    Address = forms.CharField(widget=forms.Textarea)
    Phone_no = forms.IntegerField()
    
    class Meta:
        model = UserProfile #form is saved in userprofile model
        '''
        widgets = {
            'Password' : forms.PasswordInput()
        }
        '''
        # the order in which the fields in the form are to be displayed:
        fields = [
            'Name', 'Phone_no', 'Email', 'Address', 'password1', 'password2'
        ]