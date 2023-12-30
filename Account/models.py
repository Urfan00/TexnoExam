from django.db import models
from django.contrib.auth.models import AbstractUser
from services.uploader import Uploader
from datetime import date



class Account(AbstractUser):
    username = models.CharField(max_length=7, unique=True)
    password = models.CharField(max_length=255)
    FIN = models.CharField(max_length=7, unique=True)
    image = models.ImageField(upload_to=Uploader.user_image, null=True, blank=True, max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    birthday = models.DateField(null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    first_time_login = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()

    # Your custom function to calculate age
    def calculate_age(self):
        if self.birthday:
            today = date.today()
            age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            return age
        return None

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
