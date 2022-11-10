# user/urls.py
from django.urls import path

from .views import signup, log_in, log_out,profile,editprofile
app_name = "user"
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('profile/', profile, name='profile'),
    path('editprofile/', editprofile, name='editprofile'),
]