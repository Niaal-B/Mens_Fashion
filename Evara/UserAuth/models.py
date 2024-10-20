from django.db import models
from django.utils import timezone

class OTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
