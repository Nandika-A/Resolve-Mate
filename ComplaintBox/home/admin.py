from django.contrib import admin
from .models import TaskHistory, Comment
# Register your models here.
admin.site.register(TaskHistory)
admin.site.register(Comment)