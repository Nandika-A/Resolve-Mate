
# user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.urls import reverse
from .models import UserProfile, WorkerProfile,CustomUser
from .forms import SignUpForm, LogInForm, UpdateUserForm, UpdateProfileForm, UpdateWorkerForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            django_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()   

    return render(request, 'user/signup.html', {'form': form})


def login(request):
    
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
                django_login(request, user)  
                return redirect('home')
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'user/login.html', {'form': form, 'error': error})


def logout(request):
    django_logout(request)
    return redirect(reverse('user:login'))
    

@login_required
def profile(request):
    if request.user.is_authenticated:
        
        user=request.user.email
        c=CustomUser.objects.get(email=user)
        
        u=UserProfile.objects.get(user=c)
        try:
            w=WorkerProfile.objects.get(worker=u)
        except WorkerProfile.DoesNotExist:
            w = None
        
        
        #w = get_object_or_404(WorkerProfile, worker__user__username=user)
        #u=get_object_or_404(UserProfile, user__username=user)
    return render(request, 'user/profile.html', {'w':w,'u': u,'request.user':request.user})
    #return render(request, 'user/profile.html')
def editprofile(request):
    if request.method == 'POST':
        
        user_form = UpdateUserForm(request.POST, instance=request.user)
        #profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        #worker_form=UpdateWorkerForm(request.POST,instance=request.user ) #check if .profile should be there
        
        
        if user_form.is_valid():
            
          user_form.save()
          return redirect(reverse('user:profile'))
    
        # if worker_form.is_valid():
        #     user=request.user.email
        #     c=CustomUser.objects.get(email=user)
        #     u=UserProfile.objects.get(user=c)

        #     worker1=worker_form.save()
        #     worker1.worker=WorkerProfile.objects.get(worker=u)
        #     worker1.save()           

        
    else:
        user_form = UpdateUserForm(instance=request.user)
        #profile_form = UpdateProfileForm(instance=request.user)
        #worker_form=UpdateWorkerForm(instance=request.user)
    #return render(request, 'user/editprofile.html', {'user_form': user_form, 'profile_form': profile_form, 'worker_form' : worker_form})
    return render(request, 'user/editprofile.html', {'user_form': user_form})

def editworkerprofile(request):
    if request.method == 'POST':
        
        
        worker_form=UpdateWorkerForm(request.POST,instance=request.user ) #check if .profile should be there
        
        
        
        
        if worker_form.is_valid():
            user=request.user.email
            c=CustomUser.objects.get(email=user)
            u=UserProfile.objects.get(user=c)
            worker1 = WorkerProfile()
            worker_form.save()
            worker1.worker=u 
            worker1.biodata=worker_form.cleaned_data.get("biodata")
            worker1.profession=worker_form.cleaned_data.get("profession")

            worker1.save()

            return redirect('home')

        
    else:
        #user_form = UpdateUserForm(instance=request.user)
        #profile_form = UpdateProfileForm(instance=request.user)
        worker_form=UpdateWorkerForm(instance=request.user)
    #return render(request, 'user/editprofile.html', {'user_form': user_form, 'profile_form': profile_form, 'worker_form' : worker_form})
    return render(request, 'user/editworkerprofile.html', {'worker_form': worker_form})