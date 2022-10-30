from home.views import homepage , complaintform, ProfileDetailView
from django.urls import path
from user.views import activate
urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
<<<<<<< HEAD
    path('/form', complaintform, name = 'complaintform'),
    path('/profile/<int:pk>/', ProfileDetailView.as_view(), name = 'profile-detail')
=======
#    path('/form', views.complaintform, name = 'complaintform'),
>>>>>>> 3c1c360f892e01b62f0d5bcb7b577d744c870bb2
]