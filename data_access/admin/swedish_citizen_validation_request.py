import datetime

from django.contrib import admin

from data_access.models.swedish_citizen_validation_request import SwedishCitizenValidationRequest, ValidationResult


@admin.action(description='Approve selected requests')
def approve_requests(modeladmin, request, queryset):
    queryset.update(validation_result=ValidationResult.APPROVED, validation_date=datetime.datetime.now())


@admin.action(description='Reject selected requests')
def reject_requests(modeladmin, request, queryset):
    queryset.update(validation_result=ValidationResult.REJECTED, validation_date=datetime.datetime.now())


@admin.register(SwedishCitizenValidationRequest)
class SwedishCitizenValidationRequestAdmin(admin.ModelAdmin):
    search_fields = ['user__email']
    autocomplete_fields = ['user']
    ordering = ['validation_result']
    readonly_fields = ['user', 'validation_date']
    list_display = ['user', 'validation_result']
    list_display_links = ['user', 'validation_result']
    actions = [approve_requests, reject_requests]
