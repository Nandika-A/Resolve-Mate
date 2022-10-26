from worker import views as worker_views
from django.urls import path

urlpatterns = [
    #To direct worker to register page
    path('worker_register/', worker_views.register, name = 'register_as_worker'),
]
