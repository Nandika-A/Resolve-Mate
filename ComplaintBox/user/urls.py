from user import views as user_views
from django.urls import path , include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #To direct user to register page
    path('user_register/', user_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'user/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name = 'logout'),
    path('profile/', user_views.profile, name= 'profile'),
    path('edit/', user_views.edit_profile, name= 'edit'),
    path ('',include('home.urls')),
]
#image
if settings.DEBUG:

    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
