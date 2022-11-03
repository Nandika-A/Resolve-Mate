from django.shortcuts import render, HttpResponse
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
from .models import Comment , TaskHistory 
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')
'''
    wfilter = UserProfile.objects.filter(request.GET, queryset = profiles)
    logging.info("*******",wfilter, profiles)
    #wfilter = UserProfile.Filter(request.GET, queryset = profiles)
    profiles = wfilter.qs
  '''  
    context = {
        "profiles" : profiles,
        "count" : profiles.count
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
        taskHistory.save()

    return render(request, "home/tasks.html", context)

    
class ProfileDetailView(FormMixin, DetailView):
    model = UserProfile
    def detailedprofile(request):
        context = {}
        if request.method == "POST":
            TaskHistory.profession = object.profession
            TaskHistory.complaint = request.POST.get('complaint')
            #TaskHistory.assignedby = 
            #TaskHistory.assigned = 
            TaskHistory.save()
            
# def complaintform(request):
#     context = {}
#     if request.method == "POST":
#         #TaskHistory.assignedby =
#         #TaskHistory.date_posted =  
#         TaskHistory.profession = request.POST.get('wtype')
#         TaskHistory.complaint = request.POST.get('complaint')
#         TaskHistory.status = 'ONGOING'
#         TaskHistory.save()
#     return render(request, "home/tasks.html", context)

def adminpage(request):
    tasks = TaskHistory.objects.order_by('date_posted').filter(status = 'PENDING')
    pref = UserProfile.objects.filter(username = tasks.assignedby).get('preference')
    context = {
        'tasks' : tasks,
        'pref' : pref
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