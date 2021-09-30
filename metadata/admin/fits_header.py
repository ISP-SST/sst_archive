from django.contrib import admin

from metadata.models import FITSHeader


@admin.register(FITSHeader)
class FITSHeaderAdmin(admin.ModelAdmin):
    pass
