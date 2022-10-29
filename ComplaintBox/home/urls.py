from home import views 
from django.urls import path
from user.views import activate
urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
#    path('/form', views.complaintform, name = 'complaintform'),
]