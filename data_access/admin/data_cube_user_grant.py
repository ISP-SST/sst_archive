from django.contrib import admin

from data_access.models import DataCubeUserGrant
from observations.admin import DataCubeAdmin, extend_admin
from observations.models import DataCube


@admin.register(DataCubeUserGrant)
class DataCubeUserGrantAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'user__email']
    autocomplete_fields = ['data_cube', 'user']


class DataCubeUserGrantInlineAdmin(admin.TabularInline):
    model = DataCubeUserGrant
    extra = 1


extend_admin(DataCube, DataCubeAdmin, DataCubeUserGrantInlineAdmin, weight=4)
