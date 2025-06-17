from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username=models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=250)



class UserActivityLog(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    ACTION_CHOICES = [
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("UPLOAD_FILE", "Upload File"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user.username} - {self.action} @ {self.timestamp}"


