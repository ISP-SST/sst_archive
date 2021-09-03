from django.contrib import admin

from .models import DataLocationAccessControl, DataLocationAccessGrant


@admin.register(DataLocationAccessControl)
class DataLocationAccessControlAdmin(admin.ModelAdmin):
    pass


@admin.register(DataLocationAccessGrant)
class DataLocationAccessGrantAdmin(admin.ModelAdmin):
    pass
