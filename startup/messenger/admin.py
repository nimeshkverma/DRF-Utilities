from django.contrib import admin
from messenger.models import EmailVerification


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("customer", "email_id", "email_type", "verification_code", "is_verified",
                    "times", "created_at", "updated_at",)
    list_filter = ("email_type",)
    search_fields = ("customer__customer_id", "email_id", "email_type", "verification_code", "is_verified",
                     "times", "created_at", "updated_at", )

admin.site.register(EmailVerification, EmailVerificationAdmin)
