from django.shortcuts import render, HttpResponse
#from .models import TaskHistory
# Create your views here.

def homepage(request):
    return HttpResponse("hello")
"""
def complaintform(request):
    context = {}
    if request.method == "POST":
        TaskHistory.profession = request.POST.get('')
    return render(request, "home/tasks.html", context)
    """