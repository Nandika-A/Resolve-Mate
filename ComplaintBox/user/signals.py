from django.db.models.signals import post_save
from .models import CustomUser
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile,WorkerProfile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def post_save_receiver(sender, instance, created, **kwargs):
    pass

post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)

# @receiver(post_save, sender=CustomUser)
# def save_profile(sender, instance, **kwargs):
#     instance.user.save()