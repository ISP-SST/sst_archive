from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='profile')
    affiliation = models.CharField(max_length=100, blank=True, null=True,
                                   help_text='University or research center affiliation.')
    purpose = models.CharField(verbose_name='Account purpose', max_length=190, null=True, blank=True,
                               help_text='The reason why the account was created.')
    email_verification_date = models.DateTimeField(null=True, blank=True)
    email_reverification_disabled = models.BooleanField(verbose_name='E-mail re-verification disabled', default=False,
                                                        help_text="When checked the user's email address will not need "
                                                                  "to be periodcally renewed.")

    def __str__(self):
        return "Profile for %s" % self.user.email


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
