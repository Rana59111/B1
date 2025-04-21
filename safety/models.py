# safety/models.py
from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.severity} - {self.title}"

class Camera(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    stream_url = models.URLField()
    is_active = models.BooleanField(default=True)
    has_alert = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    relationship = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.relationship})"

