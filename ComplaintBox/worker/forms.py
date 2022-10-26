from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import WorkerProfile
profession_choices = [
       'Electrician',
        'Plumber',
        'Carpenter',
        'Gardener',
        'Technician',
        'Painter',
        'Nurse'
]
#django form for user registration:
class WorkerRegistrationForm(UserCreationForm):
    #additional fields to be included in inbuilt user registration form in addition to username and password
    Name = forms.CharField()
    Email = forms.EmailField()
    Bio = forms.CharField(widget=forms.Textarea)
    Phone_no = forms.IntegerField()
    #Profession : forms.ChoiceField(choices = profession_choices)
    class Meta:
        model = WorkerProfile #form is saved in userprofile model
        # the order in which the fields in the form are to be displayed:
        fields = [
            'Name', 'Phone_no', 'Email', 'Bio', 'password1', 'password2'
        ]