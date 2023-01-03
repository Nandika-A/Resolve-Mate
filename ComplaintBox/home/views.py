from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
import logging
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from .forms import CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from asyncio import taskgroups
from .models import TaskHistory
from user.models import UserProfile, WorkerProfile
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView
from .forms import CommentForm
from .models import Comment, TaskHistory
from user.models import CustomUser 
from .decorators import admin_only
#from .filters import UserProfileFilter
from django.core.mail import send_mail
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
#html email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def home(request):
    return render(request, 'home/homepage.html')
def about(request):
    return render(request, 'home/about.html')

def homepage(request):
    
    professionfilter = WorkerProfile.objects.values_list('profession')
    l1=[]
    for x in professionfilter:
        if x[0] not in l1:
            l1+=[x[0]]
    if request.method == "GET":
        p = request.GET.get('w')
        profiles = WorkerProfile.objects.filter(profession = p).order_by('-star')
    else:
        profiles =  WorkerProfile.objects.order_by('-star')
    context = {
        'professionfilter' : professionfilter,
        'profiles' : profiles,
        'l1':l1
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

def profile_detail(request, pk):
    worker = get_object_or_404(WorkerProfile, pk=pk)
    context ={
            'worker':worker,
            # 'u':u
            }
    if request.method == "POST":
            taskHistory = TaskHistory()
            taskHistory.profession = worker.profession
            w_email = worker.worker.user.email
            taskHistory.title = request.POST.get('title')
            taskHistory.complaint = request.POST.get('complaint')
            userprofile=get_object_or_404(UserProfile,user=request.user)
            
            taskHistory.assignedby = userprofile
            taskHistory.assigned = worker
            taskHistory.Comments=" "
            taskHistory.status = 'ONGOING'
            #worker.no_of_jobs += 1
            taskHistory.save()
            
            # sending email to user after lodging complaint
            send_mail(
            'New Complaint lodged',
            'Your complaint has been successfully lodged. Kindly wait for approval.\n'+
            'Title:' + taskHistory.title + '\nComplaint:' + taskHistory.complaint+'\n',
            'basicuser338@gmail.com',
            [userprofile.user.email],
            )
            
            # sending approval email to worker
            html_content = render_to_string('email_template.html'
                                            ,
                                            {
                                                "title" : taskHistory.title,
                                                "complaint" : taskHistory.complaint,
                                               
                                             }) # render with dynamic value
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                'New Complaint lodged, send your approval.',
                'Title:' + taskHistory.title + '\nComplaint:' + taskHistory.complaint+'\n',
                'basicuser338@gmail.com',
                [w_email]
                )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    return render(request, 'home/WorkerProfile_detail.html', context)

class ProfileDetailView(DetailView):
            model = WorkerProfile
            template_name = 'WorkerProfile_detail.html'

            def get_object(self, pk):
                return get_object_or_404(WorkerProfile, pk=pk)
     #I know pk=username is not correct. I am not sure what to put pk=? 
            

# class ProfileDetailView(FormMixin, DetailView):
#     model = WorkerProfile
    # def detailedprofile(request):
        
        # if request.method == "POST":
        #     TaskHistory.profession = object.profession
        #     TaskHistory.complaint = request.POST.get('complaint')
        #     TaskHistory.assignedby = request.user.username
        #     TaskHistory.assigned = object.workername
        #     TaskHistory.status = 'ONGOING'
        #     WorkerProfile.no_of_jobs += 1
        #     TaskHistory.save()

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
        

 
def detailed_task(request, pk):
    task = get_object_or_404(TaskHistory, pk=pk)
    comments = task.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.task = task
            # Save the comment to the database
            new_comment.save()
            

    else:
        comment_form = CommentForm()
        #task = get_object_or_404(TaskHistory, pk=pk)
        # c=CustomUser.objects.get(email=user)
        
        # u=UserProfile.objects.get(user=c)
       
    return render(request, 'home/detailed_task.html', {'task':task,
                                            'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form

    })
    
    
class ComplaintUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TaskHistory
    fields = ['complaint','title']
    success_url = ''

    
    def form_valid(self, form):
        form.instance.assignedby.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        complaint = self.get_object()
        if self.request.user == complaint.assignedby.user:
            return True
        return False


class DeleteComplaintView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TaskHistory
    success_url = '/history/'

    def test_func(self):
        complaint = self.get_object()
        if self.request.user == complaint.assignedby.user:
            return True
        return False

@login_required
def displayhistory(request):
    if request.user.is_authenticated:
        
        user1=request.user
        c=CustomUser.objects.get(email=user1)
        u=UserProfile.objects.get(user=c)

        
        tasks = TaskHistory.objects.filter(assignedby = u)
        context = {
            'tasks' : tasks,
            'request.user' : request.user
            
            }      
    return render(request, 'home/displayhistory.html',context)
        
            
    