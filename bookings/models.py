from django.conf import settings
from django.db import models

#Activity Model
class Activity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    availability_status = models.BooleanField(default=True, help_text="Check if the activity is available")

    def __str__(self):
        return self.name

#Booking Model
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(default=60, help_text="Duration in minutes")
    
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="pending",
    )

    def __str__(self):
        return f"Booking by {self.user.username} for {self.activity.name} on {self.date} at {self.time}"
