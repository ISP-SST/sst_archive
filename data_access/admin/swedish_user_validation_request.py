import datetime

from django.contrib import admin

from core.models import UserProfile
from data_access.models.swedish_user_validation_request import SwedishUserValidationRequest, ValidationResult


@admin.action(description='Approve selected requests')
def approve_requests(modeladmin, request, queryset):
    queryset.update(validation_result=ValidationResult.APPROVED, validation_date=datetime.datetime.now())


@admin.action(description='Reject selected requests')
def reject_requests(modeladmin, request, queryset):
    queryset.update(validation_result=ValidationResult.REJECTED, validation_date=datetime.datetime.now())


class ValidationRequestUserInline(admin.StackedInline):
    """
    The inline admin form that is added to the User's admin page. This allows administrators to quickly view and
    change what data cubes are assigned to a specific user.
    """
    model = UserProfile
    extra = 0


@admin.register(SwedishUserValidationRequest)
class SwedishUserValidationRequestAdmin(admin.ModelAdmin):
    search_fields = ['user__email']
    autocomplete_fields = ['user']
    ordering = ['validation_result']
    list_display = ['user', 'first_name', 'last_name', 'validation_result', 'affiliation', 'purpose', 'validation_date']
    list_display_links = ['user', 'validation_result']
    actions = [approve_requests, reject_requests]
