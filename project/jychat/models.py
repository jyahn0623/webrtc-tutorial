from django.db import models

class ChatMessage(models.Model):
    message = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
