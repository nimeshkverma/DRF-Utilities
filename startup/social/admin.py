from django.contrib import admin
from social.models import Login, LinkedinProfile, SocialProfile


class LoginAdmin(admin.ModelAdmin):
    list_display = ("customer", "email_id", "platform", "source", "social_data",
                    "platform_token", "session_token", "imei", "app_registration_id", "created_at", "updated_at",)
    list_filter = ("platform", "source",)
    search_fields = ("customer__customer_id", "email_id", "platform", "source", "social_data",
                     "platform_token", "session_token", "imei", "app_registration_id", "created_at", "updated_at", )

admin.site.register(Login, LoginAdmin)


class LinkedinProfileAdmin(admin.ModelAdmin):
    list_display = ("customer", "source", "code", "state", "auth_token", "social_data", "email_id", "linkedin_id", "first_name", "last_name", "gender",
                    "profile_link", "profile_pic_link", "industry", "location", "last_employer", "join_date_last_employer", "connections", "created_at", "updated_at",)
    search_fields = ("customer__customer_id", "source", "code", "state", "auth_token", "social_data", "email_id", "linkedin_id", "first_name", "last_name", "gender",
                     "profile_link", "profile_pic_link", "industry", "location", "last_employer", "join_date_last_employer", "connections", "created_at", "updated_at",)

admin.site.register(LinkedinProfile, LinkedinProfileAdmin)


class SocialProfileAdmin(admin.ModelAdmin):
    list_display = ("customer", "email_id", "platform", "platform_id", "first_name",
                    "last_name", "gender", "profile_link", "profile_pic_link", "created_at", "updated_at",)
    list_filter = ("platform",)
    search_fields = ("customer__customer_id", "email_id", "platform", "platform_id", "first_name",
                     "last_name", "gender", "profile_link", "profile_pic_link", "created_at", "updated_at",)

admin.site.register(SocialProfile, SocialProfileAdmin)
