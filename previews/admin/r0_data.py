from django.contrib import admin

from previews.models import R0Data


@admin.register(R0Data)
class R0DataAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename']
