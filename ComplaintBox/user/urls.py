# user/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
#from .views import activate

from .views import signup, login, logout,profile,editprofile,editworkerprofile
app_name = "user"
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('editprofile/', editprofile, name='editprofile'),

    path('editworkerprofile/', editworkerprofile, name='editworkerprofile'),
    path ('',include('home.urls')),
    #    activate, name='activate'), 
#    path('accounts/', include('allauth.urls')), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)