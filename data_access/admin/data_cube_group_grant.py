from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from data_access.models import DataCubeGroupGrant
from observations.admin import extend_admin, DataCubeAdmin
from observations.models import DataCube


@admin.register(DataCubeGroupGrant)
class DataCubeGroupGrantAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'group__name']
    autocomplete_fields = ['data_cube', 'group']


class DataCubeGroupGrantInlineAdmin(admin.TabularInline):
    """
    The inline admin form for group access that is added to the DataCube's admin page.
    """
    verbose_name = 'group to the access list'
    model = DataCubeGroupGrant
    autocomplete_fields = ['group']
    extra = 0


class GroupDataCubeGrantInlineAdmin(admin.TabularInline):
    """
    The inline admin form that is added to the Group's admin page. This allows administrators to quickly view and
    change what data cubes are assigned to a certain group.
    """
    model = DataCubeGroupGrant
    verbose_name = 'DataCube to the group'
    autocomplete_fields = ['data_cube']
    extra = 0


extend_admin(DataCube, DataCubeAdmin, DataCubeGroupGrantInlineAdmin, weight=5)
extend_admin(Group, GroupAdmin, GroupDataCubeGrantInlineAdmin)
