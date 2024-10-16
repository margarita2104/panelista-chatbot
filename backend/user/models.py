from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Field used for authentication
    USERNAME_FIELD = 'email'

    # Additional fields required when using createsuperuser (USERNAME_FIELD and passwords are always required)
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)
    topics = models.TextField(blank=True)
    current_job_title = models.CharField(max_length=255, blank=True)
    career_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

