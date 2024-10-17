import json
import os

from django.conf import settings
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

    def save(self, *args, **kwargs):
        # Call the original save method to store in the database
        super(User, self).save(*args, **kwargs)

        # Define the JSON file path using Path and BASE_DIR
        json_file_path = settings.BASE_DIR / 'user' / 'speakers.json'

        # Create a dictionary representing the user
        user_data = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "topics": self.topics,
            "current_job_title": self.current_job_title,
            "career_description": self.career_description
        }

        # Check if the file exists, if it does, load the existing data
        if json_file_path.exists():
            with json_file_path.open('r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Add the new user data
        data.append(user_data)

        # Write the updated data back to the JSON file
        with json_file_path.open('w') as file:
            json.dump(data, file, indent=4)
