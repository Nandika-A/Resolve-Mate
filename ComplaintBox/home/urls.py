from home.views import homepage ,home, complaintform, ProfileDetailView, displayhistory, adminpage, complaint_detailview,about#, admin_login
from django.urls import path
from user.views import editprofile
from user import views as user_views
from .views import (

    ComplaintUpdateView,
    DeleteComplaintView
)
urlpatterns = [
    path('', home, name = 'home'),
    path('workerslist', homepage, name='homepage'),
    path('about', about, name='about'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('form', complaintform, name = 'complaintform'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name = 'profile-detail'),
    path('editprofile',user_views.editprofile, name = 'editprofile'),
    path('<int:pk>/update/', ComplaintUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', DeleteComplaintView.as_view(), name='post-delete'),
    path('history/', displayhistory, name = 'history'),
    #path('adminlogin/', admin_login, name = 'admilogin'),
    path('adminpage', adminpage, name = 'adminpage'),
    path('detailed_task/<int:pk>', complaint_detailview, name = 'complaint_detailview')
]