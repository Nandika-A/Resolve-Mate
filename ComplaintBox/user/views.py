from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .forms import Createuserform, AddDetails, AddWorkerDetails
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def register(request):
    if request.method == 'POST':
        form = Createuserform(request.POST)
        if form.is_valid():
            #save form in memoe=ry but not not in database becuase it will be saved only after the email has beeen verified
            user =form.save(commit=False)
            user.is_active=False
            user.save()
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
            username = form.cleaned_data.get('username')
            messages.success(request, f'your account has been created you can now login using {username}!')
            return redirect('login')
    else:
        form = Createuserform()
    return render(request, 'user/register.html', {'form': form})

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
        messages.success(request, f'your account has been created you can now login!')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def profile(request) :
    return render(request, 'user/profile.html')

@login_required
def  edit_profile(request):
    if request.method == 'POST':
        form = AddDetails(request.POST)
        if form.is_valid():
            user =form.save
            user.is_active=False
            user.save()
            #to get domain of current site
            
            username = form.cleaned_data.get('username')
            form1=AddWorkerDetails(request.POST)
            if form1.is_valid():
                user =form1.save
                user.is_active=False
                user.save()
                messages.success(request, f'your details has been added you can now use our website, {username}!')
                return redirect('')
    else:
        form = AddDetails()
        form1=AddWorkerDetails()
    return render(request, 'user/edit_profile.html', {'form': form})


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
                        
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})