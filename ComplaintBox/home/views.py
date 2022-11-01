from django.shortcuts import render, HttpResponse
<<<<<<< HEAD
import logging
=======
>>>>>>> 41d43cc942cc5010f9a8bdf4d4ab357d43073c43
from .models import TaskHistory
from user.models import UserProfile
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView

<<<<<<< HEAD
def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')
    wfilter = UserProfileFilter(request.GET, queryset = profiles)
    logging.info("*******",wfilter, profiles)
    profiles = wfilter.qs
    logging.info("*******",wfilter, profiles)
    print(profiles)
    print(wfilter)
=======
# Create your views here.

def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')[:10]
>>>>>>> 41d43cc942cc5010f9a8bdf4d4ab357d43073c43
    context = {
        "profiles" : profiles,
        "wfilter" : wfilter,
        "count" : profiles.count
    }
    if profiles.count==0:
<<<<<<< HEAD
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

    
=======
        #return render(request, "home/home.html")
        context = {
            "count" : 0
        }
    return render(request, "home/tasks.html", context)
    """ender(request, "home/home.html", context)
>>>>>>> 41d43cc942cc5010f9a8bdf4d4ab357d43073c43
"""
class ProfileDetailView(FormMixin, DetailView):
    model = UserProfile
    def detailedprofile(request):
        context = {}
        if request.method == "POST":
            TaskHistory.profession = object.profession
            TaskHistory.complaint = request.POST.get('complaint')
            TaskHistory.save()
            
def complaintform(request):
    context = {}
    if request.method == "POST":
        TaskHistory.profession = request.POST.get('wtype')
        TaskHistory.complaint = request.POST.get('complaint')
        TaskHistory.save()
    return render(request, "home/tasks.html", context)
<<<<<<< HEAD
    """

=======

  
    
>>>>>>> 41d43cc942cc5010f9a8bdf4d4ab357d43073c43
