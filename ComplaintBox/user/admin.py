from django.contrib import admin
from .models import UserProfile, WorkerProfile
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(WorkerProfile)