import sys

from django import forms
from django.contrib import admin

from observations.models import DataCube


class DataCubeAdminForm(forms.ModelForm):
    class Meta:
        model = DataCube
        fields = '__all__'
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }


@admin.register(DataCube)
class DataCubeAdmin(admin.ModelAdmin):
    form = DataCubeAdminForm
    list_display = ['filename', 'path', 'size']
    search_fields = ['filename']


_inlines_collection = {}


def extend_admin(root_model, root_admin, new_inline_admin, weight=sys.maxsize):
    inline_tuples = _inlines_collection.get(root_admin, [])
    inline_tuples.append((new_inline_admin, weight))

    inline_tuples.sort(key=lambda x: x[1])

    new_inlines = [t[0] for t in inline_tuples]

    class AdminAddon(root_admin):
        inlines = new_inlines

    admin.site.unregister(root_model)
    admin.site.register(root_model, AdminAddon)

    _inlines_collection[root_admin] = inline_tuples
