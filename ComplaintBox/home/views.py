from django.shortcuts import render, HttpResponse
#from .models import TaskHistory
from user/models import UserProfile
# Create your views here.

def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')
    context = {
        "profiles" : profiles
    }
    return render(request, "home/home.html", context)
"""
def complaintform(request):
    context = {}
    if request.method == "POST":
        TaskHistory.profession = request.POST.get('')
    return render(request, "home/tasks.html", context)
    """
    
