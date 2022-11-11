from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser,UserProfile,WorkerProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields =("username", "email")

class UpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    #bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    phone_no=forms.CharField()
    address=forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = UserProfile
        fields = ['image', 'phone_no','address']

class UpdateWorkerForm(forms.ModelForm):
    biodata= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    profession=forms.CharField()
    
    class Meta:
        model = WorkerProfile
        fields = ['biodata', 'profession']