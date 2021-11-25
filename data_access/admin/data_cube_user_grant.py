from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.utils import extend_admin
from data_access.models import DataCubeUserGrant
from observations.admin import DataCubeAdmin
from observations.models import DataCube


@admin.register(DataCubeUserGrant)
class DataCubeUserGrantAdmin(admin.ModelAdmin):
    """
    Main admin form for DataCubeUserGrants.
    """
    search_fields = ['data_cube__filename', 'user_email']
    autocomplete_fields = ['data_cube']


class DataCubeUserGrantInlineAdmin(admin.TabularInline):
    """
    The inline admin form that is added to the DataCube's admin page.
    """
    verbose_name = 'user to the access list'
    model = DataCubeUserGrant
    extra = 0


extend_admin(DataCube, DataCubeAdmin, DataCubeUserGrantInlineAdmin, weight=4)
