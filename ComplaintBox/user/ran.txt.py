from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.db import transaction

from user.models import UserProfile
from .forms import Createuserform,UserProfileForm
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        form = Createuserform(request.POST)
        if form.is_valid():
            #save form in memoe=ry but not not in database becuase it will be saved only after the email has beeen verified
            form.save(commit=False)
            #optional = form_2.save(commit = False)
            username = form.cleaned_data.get('username')
            role = form.cleaned_data.get('role')
            image=form.cleaned_data.get('image')  #images will get saved in directory called profile_pics
            phone_no= form.cleaned_data.get('phone_no')
            address = form.cleaned_data.get('address')
            biodata = form.cleaned_data.get('biodata')
            user = User.objects.get(username=username)
            user_data = UserProfile.objects.create(user=user, biodata=biodata,address=address,phone_no=phone_no,image=image,role=role)
            user_data.save()
            #to get domain of current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete registration')
            # username = form.cleaned_data.get('username')
            # messages.success(request, f'your account has been created you can now login using {username}!')
            # return redirect('login')
    else:
        form = Createuserform()
        #form_2 = Userform()
    return render(request, 'user/register.html', {'form': form} )

def activate(request,uidb64,token):
    User=get_user_model()
    try:
        uid=uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True #mean user can login
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def profile(request) :
    return render(request, 'user/profile.html')


# @login_required
# @transaction.atomic
# def edit_profile(request):
#     if request.method=='POST':
#         form = Createuserform(request.POST, instance=request.user)
        

#         if form.is_valid():
#             form.save(commit=False)
#             username = form.cleaned_data.get('username')
#             role = form.cleaned_data.get('role')
#             image=form.cleaned_data.get('image')  #images will get saved in directory called profile_pics
#             phone_no= form.cleaned_data.get('phone_no')
#             address = form.cleaned_data.get('address')
#             biodata = form.cleaned_data.get('biodata')
#             user = User.objects.get(username=username)
#             user_data = UserProfile.objects.create(user=user, biodata=biodata,address=address,phone_no=phone_no,image=image,role=role)
#             user_data.save()
#             return redirect('/account/profile')
#     else:
#         profile_form = UserProfileForm(instance=request.user.userprofile)
#         user_form = Createuserform(instance=request.user)
#     args = {
#         'user_form': user_form, # basic user form
#         'profile_form': profile_form # user profile form
#         }
#     return render(request, 'accounts/edit_profile.html', args)