# user/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
#from .views import activate

from .views import signup, log_in, log_out,profile,editprofile
app_name = "user"
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('profile/', profile, name='profile'),
    path('editprofile/', editprofile, name='editprofile'),
    path ('',include('home.urls')),
    #    activate, name='activate'), 
#    path('accounts/', include('allauth.urls')), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)