from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import WorkerRegistrationForm
from django.contrib.auth.hashers import make_password, check_password
def register(request):
    if request.method == "POST":
        wform = WorkerRegistrationForm(request.POST) #created in user/forms.py
        if wform.is_valid():
            '''
            hashed_pwd = make_password("plain_text")
            if check_password("plain_text", hashed_pwd):
            
            form.password = make_password('password')
            '''
            wform.save()
            #worker will be redirected to home page after registration
            return redirect('homepage')
    else:
        wform = WorkerRegistrationForm()
        #showing html page(register.html)
        return render(request, 'worker/register.html', {
        "wform" : wform
    })
