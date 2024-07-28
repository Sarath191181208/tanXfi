from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    """
    Model to represent an Alert for a specific cryptocurrency and target price.

    An Alert is associated with a user and has a status indicating its current state.
    """
    STATUS_CHOICES = [
        ("created", "Created"),   # Alert has been created but not yet triggered
        ("triggered", "Triggered"),  # Alert has been triggered when the target price is reached
        ("deleted", "Deleted"),    # Alert has been deleted
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='alerts',
        help_text="The user associated with this alert."
    )
    coin = models.CharField(
        max_length=10,
        default="btcusdt",
        help_text="The cryptocurrency pair for this alert (e.g., 'btcusdt')."
    )
    target_price = models.FloatField(
        help_text="The target price at which the alert is triggered."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created",
        help_text="The current status of the alert."
    )

    def __str__(self):
        """
        Return a string representation of the Alert instance.

        Format:
            "{user's name} - {coin} at ${target_price}"
        """
        return f"{self.user.username} - {self.coin} at ${self.target_price}"
