from django.shortcuts import render, HttpResponse
from .models import TaskHistory
from user.models import UserProfile
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView

# Create your views here.

def homepage(request):
    profiles = UserProfile.objects.filter(role = 'WORKER').order_by('Star__0')[:10]
    context = {
        "profiles" : profiles,
        "wfilter" : wfilter,
        "count" : profiles.count
    }
    if profiles.count==0:
        #return render(request, "home/home.html")
        context = {
            "count" : 0
        }
    return render(request, "home/tasks.html", context)
    """ender(request, "home/home.html", context)
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

  
    
