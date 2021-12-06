from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
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

# Remove the social parts of the django-allauth application from the admin interface.
# We don't use the social parts, but we can't remove that app completely since there are
# apparently dependencies from the core part of allauth.
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
