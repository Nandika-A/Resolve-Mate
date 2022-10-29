from django.shortcuts import render, HttpResponse
#from .models import TaskHistory
from user.models import UserProfile
# Create your views here.

def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')[:10]
    context = {
        "profiles" : profiles
    }
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
    
