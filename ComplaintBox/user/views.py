from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
#to display success message to the user after registration on home page
from .forms import UserRegistrationForm
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST) #created in user/forms.py
        if form.is_valid():
            #to get the username from the form to display it in the message
            username = form.cleaned_data.get('username')
            # to show success message
            messages.success(request,f'Account created for {username}!')
            form.save()
            #user will be redirected to home page after registration
            return redirect('#')
    else:
        form = UserRegistrationForm()
        #showing html page(register.html)
        return render(request, 'user/register.html', {
        "form" : form
    })
