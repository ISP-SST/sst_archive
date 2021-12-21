from django.contrib import admin

from observations.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
