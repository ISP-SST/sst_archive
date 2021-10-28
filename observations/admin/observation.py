from django.contrib import admin

from observations.models import Observation


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ['point_id']
    search_fields = ['point_id']
