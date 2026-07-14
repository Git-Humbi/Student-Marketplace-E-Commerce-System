from django.contrib.auth.models import AbstractUser
from django.db import models


# username, password, first_name, last_name, is_staff, is_active, is_superuser, last_login, date_joined imported from AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)
    otp_code_hash = models.CharField(max_length=255, null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(email__iregex=r"@kabarak\.ac\.ke$"),
                name="email_must_be_kabarak_domain",
            )
        ]

    def __str__(self):
        return self.username
    