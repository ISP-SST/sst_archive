from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields

from core.models import UserProfile
from core.utils import extend_admin


class CustomUserCreationForm(UserCreationForm):
    verify_email = fields.BooleanField(
        label="Verify e-mail",
        help_text="Check if you want to automatically mark this e-mail as verified in the system.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(username=email).exists():
            raise ValidationError(
                'This email is already assigned to an existing user.',
                code='email_taken',
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=True)
        email = user.email

        # Force username to e-mail.
        user.username = email
        user.save()

        if self.cleaned_data['verify_email']:
            email_address, created = EmailAddress.objects.get_or_create(
                user=user, email__iexact=email, defaults={"email": email, "verified": True, "primary": True}
            )

        return user


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


class UserProfileInlineAdmin(admin.StackedInline):
    model = UserProfile
    can_delete = False
    min_num = 1
    max_num = 1
    fields = ['affiliation', 'purpose', 'email_verification_date', 'email_reverification_disabled']
    readonly_fields = ['email_verification_date']


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = ((None, {
        'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'verify_email'),
        'classes': ('wide',)
    }),)


extend_admin(User, UserAdmin, UserProfileInlineAdmin, weight=0)

# Remove the social parts of the django-allauth application from the admin interface.
# We don't use the social parts, but we can't remove that app completely since there are
# apparently dependencies from the core part of allauth.
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
