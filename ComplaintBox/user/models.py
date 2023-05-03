from django.db import models
from django.core.validators import MaxValueValidator
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from PIL import Image 
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)
class CustomUser(AbstractUser):
    
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)
    
    USERNAME_FIELD = "email" # make the user log in with the email
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser,null =True, on_delete=models.CASCADE)
    
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')  #images will get saved in directory called profile_pics
    
    # Star= models.JSONField(
    #     models.DecimalField(blank=True, validators=[
    #         MaxValueValidator(5)], decimal_places = 2, max_digits = 3),
    #     default = []
    # )
    phone_no= models.CharField(default='0000',max_length=50)
    address = models.TextField(default = '0000')
    #star=models.DecimalField(max_digits=3,decimal_places=2,default=5.00)
    # preference= JSONField(
    #     models.DecimalField(blank=True, validators=[
    #         MaxValueValidator(5)], decimal_places = 2, max_digits = 3),
    #     size=2,default = None
    # )
    def __str__(self):
        return self.user.username
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class WorkerProfile(models.Model):
    worker =models.OneToOneField(UserProfile, null =True, on_delete=models.SET_NULL)
    profession = models.CharField(max_length=100, default=None)
    biodata = models.TextField(default = None)
    no_of_jobs = models.IntegerField(default=0)
    upi=models.CharField(max_length=50,default=None)

    #average_star=models.DecimalField(max_digits=3,decimal_places=2,default=5.00)
    #UPI = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.worker.user.username

class Rating(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3,decimal_places=2,default=5.00)
    #star=models.DecimalField(max_digits=3,decimal_places=2,default=5.00)

    def __str__(self):
        return f"{self.Worker}: {self.rating}"
