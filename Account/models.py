from django.db import models
from django.contrib.auth.models import AbstractUser
from Exam.models import CourseTopic
from services.mixins import DateMixin
from services.uploader import Uploader
from datetime import date



class Account(AbstractUser):
    username = models.CharField(max_length=7, unique=True)
    FIN = models.CharField(max_length=7, unique=True)
    image = models.ImageField(upload_to=Uploader.user_image, null=True, blank=True, max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    birthday = models.DateField(null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    first_time_login = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'FIN']

    def __str__(self):
        return self.get_full_name()

    # Your custom function to calculate age
    def calculate_age(self):
        if self.birthday:
            today = date.today()
            age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            return age
        return None

    def save(self, *args, **kwargs):
        # Set the password to be equal to the FIN code when the instance is created
        if not self.pk:  # Check if the instance is being created (not updated)
            self.set_password(self.FIN)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class StudentResult(DateMixin):
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    point_1 = models.PositiveIntegerField(default=0)
    point_2 = models.PositiveIntegerField(default=0)
    point_3 = models.PositiveIntegerField(default=0)
    total_point = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    exam_topics = models.ManyToManyField(CourseTopic)

    def save(self, *args, **kwargs):
        self.total_point = self.point_1 + self.point_2 + self.point_3
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.get_full_name()} result"

    class Meta:
        verbose_name = 'Student Result'
        verbose_name_plural = 'Student Result'
