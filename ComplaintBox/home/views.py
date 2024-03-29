from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.db.models import Avg
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
from user.models import UserProfile, WorkerProfile,Rating
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
from .forms import CHOICES
import random

#automatic assigning
from queue import PriorityQueue


def home(request):
    return render(request, 'home/home.html')
def about(request):
    return render(request, 'home/about.html')

def workerslist(request):
    
    professionfilter = WorkerProfile.objects.values_list('profession')
    list1=[]
    for profession_received in professionfilter:
        if profession_received[0] not in list1:
            list1+=[profession_received[0]]
    if request.method == "GET":
        profession = request.GET.get('worker')
        profiles = WorkerProfile.objects.filter(profession = profession)
    else:
        profiles =  WorkerProfile.objects.order_by('-star')
    context = {
        'professionfilter' : professionfilter,
        'profiles' : profiles,
        'list1':list1
    }
    if profiles.count==0:
        return render(request, "home/workerslist.html")

    return render(request, "home/workerslist.html", context)    
    

def complaintform(request):
    professionfilter = WorkerProfile.objects.values_list('profession')
    list1=[]
    for profession_received in professionfilter:
        if profession_received[0] not in list1:
            list1+=[profession_received[0]]
    context = {"list1":list1}
    # print(request)
    # print(request.POST)
    if request.method == "POST":
        # print("wfk0")
        # print(request.user)
        taskHistory = TaskHistory()
        taskHistory.profession = request.POST.get('wtype')
        # print(taskHistory.profession)
        taskHistory.title = request.POST.get('title')
        taskHistory.complaint = request.POST.get('complaint')
        taskHistory.assignedby = UserProfile.objects.get(user=request.user)
        taskHistory.save()
        # send_mail(
        #     'Complaint lodged',
        #     'Your complaint has been successfully lodged.\n'+
        #     'Title:' + taskHistory.title + '\nComplaint:' + taskHistory.complaint+'\n',
        #     'basicuser338@gmail.com',
        #     [taskHistory.assigned_by.user.email],
        #     )
        

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
            #worker.no_of_jobs += 1
            taskHistory.save()
            
            #sending email to user after lodging complaint
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
                                                "id" : taskHistory.id
                                               
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
    tasks = TaskHistory.objects.filter(status = 'PENDING').order_by('date_posted')
    #pref = UserProfile.objects.filter(user_id = TaskHistory.assignedby.id).get('preference')
    context = {
        'tasks' : tasks,
        #'pref' : pref,
        #'worker' : worker
    }
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
    if request.method =='GET': #and 'completed' in request.post:
        task.status='COMPLETED'
        task.save()
        send_mail(
            'Thank you for using our service',
            'Please rate '+task.assigned.worker.user.username+'\n',
            'manojiyer445@gmail.com',
            [request.user.email],
            )
        #sending mail to user
        html_content = render_to_string('rating_template.html'
                                            ,
                                            {
                                                "image" : task,
                                                "username" : task,
                                                "worker" : task,
                                                "task":task,
                                                #"id" : taskHistory.id
                                               
                                             }) # render with dynamic value
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
                'Thank you for using our service, please rate us!.',
                'Title:' + task.title +'\n',
                'manojiyer445338@gmail.com',
                [request.user.email]
                )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        
    else:
        #comment_form = CommentForm()
        task = get_object_or_404(TaskHistory, pk=pk)
        # c=CustomUser.objects.get(email=user)
        
        # u=UserProfile.objects.get(user=c)
       
    return render(request, 'home/detailed_task.html', {'task':task,
                                        #     'comments': comments,
                                        #    'new_comment': new_comment,
                                        #    'comment_form': comment_form

    })
    
def rate(request, pk):
    #post = Post.objects.get(id=post_id)
    rating=Rating()
    worker=TaskHistory.objects.get(id=pk)
    average=Rating.objects.filter(Worker=worker.assigned).aggregate(Avg('rating'))
    user=worker.assignedby.user.id
    checkrating=Rating.objects.filter(Worker=worker.assigned,user=user)
    useremail=CustomUser.objects.filter(id=user)
    if request.method == "POST":
        ratingnum=request.POST.get('ratingnum')
    
        checkrating.delete()
        newrate=Rating()
        newrate.user=useremail.first()
        newrate.rating=ratingnum
        newrate.Worker=worker.assigned
        newrate.save()

    
    return render(request, 'home/rating.html', {'worker':worker.assigned,
                                                'user':user,
                                             'average': average['rating__avg'],
                                             'checkrating': checkrating.first,
                                        #    'new_comment': new_comment,
                                        #    'comment_form': comment_form

    }
    )


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
    else:
        return render(request, 'home/loginerror.html') 
    return render(request, 'home/displayhistory.html',context)
        
def approve(request, pk):
    task = get_object_or_404(TaskHistory, pk=pk)
    form = CHOICES(request.POST)
    adminemail = [
        #'eleensmathew@gmail.com',
        'nandikaagrawal610@gmail.com',
    ]
    if form.is_valid():
        selected = form.cleaned_data.get("NUMS")
        if selected == "approve":
            send_mail(
            'Complaint approved.',
            'Your complaint has been approved.\n'+
            'Title:' + task.title + '\nComplaint:' + task.complaint+'\n'
            + 'Selected employee will arrive your place within 1hr.'
            + '\nEmployee\'s name:' + task.assigned.worker.user.username,
            '@gmail.com',
            [task.assignedby.user.email],
            )
            send_mail(
                'Task approved',
                'Kindly reach within 1hr.' +
                '\nAddress:' +task.assignedby.address+
                '\nComplaint:'+ task.complaint,
                'basicuser338@gmail.com',
                [task.assigned.worker.user.email],
            )
            task.status='ONGOING'
        else:
            send_mail(
                'Task rejected',
                'The employee '+ task.assigned.worker.user.username
                +'\nID '+ str(task.assigned.id) + 
                ' rejected to work on complaint: ' + task.complaint +
                '\n Assign another employee for the same.',
                'basicuser338@gmail.com',
                adminemail,
            )
            task.assigned = None
            
    return render(request, 'home/approve.html',
                  {
                      "task" : task,
                      "form" : form
                  })  

  
def taskpage(request, pk):
    task = get_object_or_404(TaskHistory, pk=pk)
    worker = WorkerProfile.objects.filter(profession=task.profession).order_by('no_of_jobs')
    context = {
        'task':task,
        'worker':worker
    }
    if request.method == 'POST':
        work = request.POST.get('work')
        # print(work)
        task.assigned.worker.user.username = work
        wemail = task.assigned.worker.user.email
        task.status='ASSIGNED'
        task.assigned.no_of_jobs += 1
        task.save()
        task.assigned.save()
        send_mail(
                'New task',
                'Kindly reach within 1hr.' +
                '\nAddress:' +task.assignedby.address+
                '\nComplaint:'+ task.complaint,
                'basicuser338@gmail.com',
                [wemail],
            )
        send_mail(
                'Worker assigned',
                'Your complaint has been approved.\n'+
                'Title:' + task.title + '\nComplaint:' + task.complaint+'\n'
                + 'Selected employee will arrive your place within 1hr.'
                + '\nEmployee\'s name: ' + task.assigned.worker.user.username,
                'basicuser338@gmail.com',
                [task.assignedby.user.email],
            )
    return render(request, 'home/taskpage.html', context)

def automaticassign(request):
    context = {}
    if request.method == "POST":
        taskHistory = TaskHistory()
        taskHistory.profession = request.POST.get('wtype')
        taskHistory.title = request.POST.get('title')
        taskHistory.complaint = request.POST.get('complaint')
        userprofile=get_object_or_404(UserProfile,user=request.user)
        taskHistory.assignedby = userprofile
        # #workers = [str(elem) for elem in list(WorkerProfile.objects.filter(profession = taskHistory.profession).values_list('worker.user.username'))]
        # workers = WorkerProfile.objects.filter(profession = taskHistory.profession)
        # min = 100
        # selected = []
        # for w in workers:
        #     if w.no_of_jobs <= min:
        #         min = w.no_of_jobs
        #         selected += [w]
                
        # max = 0.00
        # maxrating = []
        # for s in selected:
        #     getrating = Rating.objects.get(Worker = s)
        #     if getrating.rating >= max:
        #         max = getrating.rating
        #         maxrating += [s]
        # length = len(maxrating)
        
        # if length == 1:
        #     Reqworker = maxrating[0]
        # else:
        #     i = random.randint(0,length-1)
        #     Reqworker = maxrating[i]
        
        # taskHistory.assigned = Reqworker
        # taskHistory.assigned.no_of_jobs += 1
        # taskHistory.save()
        # taskHistory.assigned.save()
        
        q = PriorityQueue()
        workers = WorkerProfile.objects.filter(profession = taskHistory.profession)
        min = 100
        selected = []
        for w in workers:
            getrating = Rating.objects.get(Worker = w)
            hfw = getrating.rating/2 - w.no_of_jobs
            q.put((hfw, w))
        first = q.get()
        obj = first[1]
        taskHistory.assigned = obj
        taskHistory.assigned.no_of_jobs += 1
        taskHistory.Comments = " "
        taskHistory.save()
        taskHistory.assigned.save()
        taskHistory.assignedby.save()
        send_mail(
                'New task',
                'Kindly reach within 1hr.' +
                '\nAddress:' +taskHistory.assignedby.address+
                '\nComplaint:'+ taskHistory.complaint,
                'basicuser338@gmail.com',
                [taskHistory.assigned.worker.user.email],
            )
        send_mail(
            'Complaint lodged',
            'Your complaint has been successfully lodged.\n'+
            'Title:' + taskHistory.title + '\nComplaint:' + taskHistory.complaint+'\n'
            + 'Selected employee will arrive your place within 1hr.'
                + '\nEmployee\'s name: ' + taskHistory.assigned.worker.user.username,
            'basicuser338@gmail.com',
            [taskHistory.assigned_by.user.email],
            )
    return render(request, "home/tasks.html", context)