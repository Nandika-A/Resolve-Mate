from home.views import homepage , complaintform, ProfileDetailView
from django.urls import path
from user.views import activate, edit_profile
from user import views as user_views
from .views import (

    ComplaintUpdateView,
    DeleteComplaintView
)
urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('form', complaintform, name = 'complaintform'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name = 'profile-detail'),
    path('edit_profile/<int:pk>/',user_views.edit_profile, name = 'edit_profile'),
    path('<int:pk>/update/', ComplaintUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', DeleteComplaintView.as_view(), name='post-delete'),
]