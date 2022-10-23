from user import views as user_views
from django.urls import path

urlpatterns = [
    #To direct user to register page
    path('user_register/', user_views.register, name = 'register_as_user'),
]
