from user import views as user_views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    #To direct user to register page
    path('user_register/', user_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'user/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name = 'logout'),
    path('profile/', user_views.profile, name= 'profile')
]

