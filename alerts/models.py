from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Alert(models.Model):
    STATUS_CHOICES = [
        ("created", "Created"),
        ("triggered", "Triggered"),
        ("deleted", "Deleted"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.CharField(max_length=10)
    target_price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")

    def __str__(self):
        return f"{self.user.name} - {self.coin} at ${self.target_price}"
