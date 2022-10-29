from django.shortcuts import render, HttpResponse
<<<<<<< HEAD
from .models import TaskHistory
from user.models import UserProfile
from .filters import UserProfileFilter
# Create your views here.

def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')
    wfilter = UserProfileFilter(request.GET, queryset = profiles)
    profiles = wfilter.qs
=======
#from .models import TaskHistory
from user.models import UserProfile
# Create your views here.

def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')[:10]
>>>>>>> 36563504d42540829b90765a74b1798761fce55f
    context = {
        "profiles" : profiles,
        "wfilter" : wfilter
    }
<<<<<<< HEAD
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
    if profiles.count==0:
        return render(request, "home/home.html")
    return render(request, "home/tasks.html", context)
    """ender(request, "home/home.html", context)
"""
def complaintform(request):
    context = {}
    if request.method == "POST":
        TaskHistory.profession = request.POST.get('')
    return r
>>>>>>> 36563504d42540829b90765a74b1798761fce55f
    
