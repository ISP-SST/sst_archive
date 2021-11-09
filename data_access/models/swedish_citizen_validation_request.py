import datetime

from django.contrib.auth.models import User, Group
from django.db import models

from data_access.models import DataCubeGroupGrant

SWEDISH_CITIZENS_GROUP = 'Swedish Citizen'


def get_swedish_citizens_group():
    group, _ = Group.objects.get_or_create(name=SWEDISH_CITIZENS_GROUP)
    return group


def enqueue_swedish_user_registration_request(user):
    request, created = SwedishCitizenValidationRequest.objects.get_or_create(user=user)


def add_user_to_swedish_citizens_group(user):
    group = get_swedish_citizens_group()
    group.user_set.add(user)
    group.save()


def is_user_in_swedish_citizens_group(user):
    group = get_swedish_citizens_group()
    return user.groups.filter(pk=group.id).exists()


def is_data_cube_restricted_to_swedish_users(data_cube):
    swedish_group = get_swedish_citizens_group()
    return data_cube.group_grants.filter(group_id=swedish_group.id).count()


def get_user_swedish_citizen_validation_status(user):
    try:
        request = SwedishCitizenValidationRequest.objects.get(user=user)
        return request.validation_result
    except SwedishCitizenValidationRequest.DoesNotExist:
        return None


def remove_user_from_swedish_citizens_group(user):
    group = get_swedish_citizens_group()
    group.user_set.remove(user)
    group.save()


class ValidationResult(models.TextChoices):
    NOT_PROCESSED = 'Not Processed'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'


class SwedishCitizenValidationRequest(models.Model):
    user = models.OneToOneField(User, verbose_name='Swedish citizen validation request', on_delete=models.CASCADE)
    validation_date = models.DateTimeField(verbose_name='Time and date when validation took place', null=True,
                                           blank=True)
    validation_result = models.TextField(verbose_name='Validation result', choices=ValidationResult.choices,
                                         default=ValidationResult.NOT_PROCESSED)

    def save(self, *args, **kwargs):
        self.validation_date = datetime.datetime.now()

        super().save(*args, **kwargs)

        if self.validation_result == ValidationResult.APPROVED:
            add_user_to_swedish_citizens_group(self.user)
        else:
            remove_user_from_swedish_citizens_group(self.user)

    def delete(self, *args, **kwargs):
        remove_user_from_swedish_citizens_group(self.user)

        super().delete(*args, **kwargs)

    def __str__(self):
        return  '%s - %s' %  (self.user.email, self.validation_result)
