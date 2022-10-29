from django.shortcuts import render, HttpResponse
from .models import TaskHistory
from user.models import UserProfile
from .filters import UserProfileFilter
# Create your views here.

def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')
    wfilter = UserProfileFilter(request.GET, queryset = profiles)
    profiles = wfilter.qs
    context = {
        "profiles" : profiles,
        "wfilter" : wfilter
    }
    return render(request, "home/home.html", context)

def complaintform(request):
    context = {}
    if request.method == "POST":
        taskHistory = TaskHistory()
        taskHistory.profession = request.POST.get('wtype')
        taskHistory.complaint = request.POST.get('complaint')
        taskHistory.save()
    return render(request, "home/tasks.html", context)
    
    
