from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Verification",
            {
                "fields": (
                    "is_email_verified",
                    "otp_code_hash",
                    "otp_expires_at",
                )
            },
        ),
    )
    list_display = ("username", "email", "is_email_verified", "is_staff")


admin.site.register(User, UserAdmin)
