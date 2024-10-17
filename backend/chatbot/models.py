from django.db import models


class Chatbot(models.Model):
    user_prompt = models.TextField(max_length=500, blank=True, null=True)
    chatbot_response = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chatbot prompt: {self.user_prompt} | Created at: {self.created_at}"
