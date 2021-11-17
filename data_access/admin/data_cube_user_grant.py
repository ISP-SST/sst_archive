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
    search_fields = ['data_cube__filename', 'user__email']
    autocomplete_fields = ['data_cube', 'user']


class DataCubeUserGrantInlineAdmin(admin.TabularInline):
    """
    The inline admin form that is added to the DataCube's admin page.
    """
    verbose_name = 'user to the access list'
    model = DataCubeUserGrant
    autocomplete_fields = ['user']
    extra = 0


class UserDataCubeGrantInlineAdmin(admin.TabularInline):
    """
    The inline admin form that is added to the User's admin page. This allows administrators to quickly view and
    change what data cubes are assigned to a specific user.
    """
    model = DataCubeUserGrant
    autocomplete_fields = ['data_cube']
    extra = 0


extend_admin(DataCube, DataCubeAdmin, DataCubeUserGrantInlineAdmin, weight=4)
extend_admin(User, UserAdmin, UserDataCubeGrantInlineAdmin)
