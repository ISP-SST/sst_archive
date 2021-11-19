from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import UserProfile
from core.utils import extend_admin


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


class UserProfileInlineAdmin(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ['affiliation', 'purpose', 'email_verification_date', 'email_reverification_disabled']
    readonly_fields = ['email_verification_date']


extend_admin(User, UserAdmin, UserProfileInlineAdmin, weight=0)
