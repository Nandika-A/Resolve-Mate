from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
import logging
from django.shortcuts import redirect
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from asyncio import taskgroups
from .models import TaskHistory
from user.models import UserProfile, WorkerProfile
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView
from .forms import CommentForm
from .models import Comment, TaskHistory 
from .decorators import admin_only
#from .filters import UserProfileFilter
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def home(request):
    return render(request, 'home/homepage.html')
    
def homepage(request):
    '''
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')
    pf = profiles.worker_profile_set.all()
    wfilter = UserProfileFilter(request.GET, queryset=pf)
    logging.info("*******",wfilter, profiles)
    wfilter = UserProfileFilter(request.GET, queryset = profiles)
    pf = wfilter.qs  
    context = {
        "profiles" : profiles,
        #"pf" : pf,
        "count" : profiles.count
    }
    '''
    professionfilter = WorkerProfile.objects.values_list('profession')
    if request.method == "GET":
        p = request.GET.get('w')
        profiles = WorkerProfile.objects.filter(profession = p).order_by('Star')
    else:
        profiles =  WorkerProfile.objects.order_by('Star')
    context = {
        'professionfilter' : professionfilter,
        'profiles' : profiles
    }
    if profiles.count==0:
        return render(request, "home/home.html")

    return render(request, "home/home.html", context)    
    

def complaintform(request):
    context = {}
    if request.method == "POST":
        taskHistory = TaskHistory()
        taskHistory.profession = request.POST.get('wtype')
        taskHistory.complaint = request.POST.get('complaint')
        taskhistory.assigned_by = request.user.username
        taskHistory.save()

    return render(request, "home/tasks.html", context)

    
class ProfileDetailView(FormMixin, DetailView):
    model = WorkerProfile
    def detailedprofile(request):
        context = {}
        if request.method == "POST":
            TaskHistory.profession = object.profession
            TaskHistory.complaint = request.POST.get('complaint')
            TaskHistory.assignedby = request.user.username
            TaskHistory.assigned = object.workername
            TaskHistory.status = 'ONGOING'
            WorkerProfile.no_of_jobs += 1
            TaskHistory.save()

@admin_only            
def adminpage(request):
    tasks = TaskHistory.objects.order_by('date_posted').filter(status = 'PENDING')
    pref = UserProfile.objects.filter(user_id = TaskHistory.assignedby.id).get('preference')
    worker = WorkerProfile.objects.filter(profession = tasks.profession).order_by('no_of_jobs')
    context = {
        'tasks' : tasks,
        'pref' : pref,
        'worker' : worker
    }
    
    if request.method == 'POST':
        TaskHistory.assigned = request.POST.get('worker')
        TaskHistory.status = 'ONGOING'
        TaskHistory.save()
    return render(request, "home/adminpage.html", context)
        

 
def complaint_detailview(request, id):
   
 if request.method == 'POST':
    cf = CommentForm(request.POST or None)
    if cf.is_valid():
      content = request.POST.get('content')
      comment = Comment.objects.create(post = TaskHistory, user = request.user, content = content)
      comment.save()
      return redirect(TaskHistory.get_absolute_url())
    else:
      cf = CommentForm()
       
    context ={
      'comment_form':cf,
      }
    return render(request, 'home / complaint_detail.html', context)
  
    
class ComplaintUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TaskHistory
    fields = ['complaint','title']
    success_url = ''

    def form_valid(self, form):
        form.instance.assignedby = self.request.user
        return super().form_valid(form)

    def test_func(self):
        complaint = self.get_object()
        if self.request.user == complaint.assignedby:
            return True
        return False

class DeleteComplaintView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TaskHistory
    success_url = ''

    def test_func(self):
        complaint = self.get_object()
        if self.request.user == complaint.author:
            return True
        return False
    
def displayhistory(request):
    tasks = TaskHistory.objects.filter(assignedby_id = request.user.id)
    context = {
        'tasks' : tasks
    }      
    return render(request, 'home/displayhistory.html', context)
    
        
            
    