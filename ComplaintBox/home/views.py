from django.shortcuts import render, HttpResponse
import logging
from .models import TaskHistory
from user.models import UserProfile
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView

def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')
    wfilter = UserProfile.objects.filter(request.GET, queryset = profiles)
    logging.info("*******",wfilter, profiles)
    profiles = wfilter.qs
    logging.info("*******",wfilter, profiles)
    print(profiles)
    print(wfilter)
# Create your views here.
'''
def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')[:10]
    context = {
        "profiles" : profiles,
        "wfilter" : wfilter,
        "count" : profiles.count
    }
    if profiles.count==0:
        return render(request, "home/home.html")

    return render(request, "home/home.html", context)    
    
'''

    
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
            
def complaintform(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            #TaskHistory.assignedby =
            #TaskHistory.date_posted =  
            TaskHistory.profession = request.POST.get('wtype')
            TaskHistory.complaint = request.POST.get('complaint')
            TaskHistory.status = 'ONGOING'
            TaskHistory.save()
        return render(request, "home/tasks.html", context)
    else:
        return redirect('login')

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
        

  
    
