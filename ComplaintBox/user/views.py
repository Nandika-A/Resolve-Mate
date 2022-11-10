
# user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .models import Userdetails, WorkerDetails
from .forms import SignUpForm, LogInForm, UpdateUserForm, UpdateProfileForm, UpdateWorkerForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()   
    return render(request, 'user/signup.html', {'form': form})


def log_in(request):
    error = False
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)  
                return redirect('home')
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'user/login.html', {'form': form, 'error': error})


def log_out(request):
    logout(request)
    return redirect(reverse('user:login'))

from django.contrib.auth.decorators import login_required




@login_required
def profile(request):
    if request.user.is_authenticated:
        user=request.user.email
        u=Userdetails.objects.filter(user__email=user)
        w=WorkerDetails.objects.filter(worker__user__email=user)
        
        #w = get_object_or_404(WorkerDetails, worker__user__username=user)
        #u=get_object_or_404(Userdetails, user__username=user)
    return render(request, 'user/profile.html', {'w':w,'u': u})
    #return render(request, 'user/profile.html')
def editprofile(request):
    if request.method == 'POST':
        #user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        #worker_form=UpdateWorkerForm(request.POST,request.user ) #check if .profile should be there
        
        
        # if user_form.is_valid():
            
        #     user_form.save()
            
        if profile_form.is_valid():
            profile_form.save()
            
        # if worker_form.is_valid():
        #     worker_form.save()
            
            return redirect(to='profile')
    else:
        #user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user)
        #worker_form=UpdateWorkerForm(instance=request.user)
    #return render(request, 'user/editprofile.html', {'user_form': user_form, 'profile_form': profile_form, 'worker_form' : worker_form})
    return render(request, 'user/editprofile.html', {'profile_form': profile_form})