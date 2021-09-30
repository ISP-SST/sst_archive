from django import forms
from django.contrib import admin

from observations.models import DataCube


class DataCubeAdminForm(forms.ModelForm):
    class Meta:
        model = DataCube
        fields = '__all__'
        widgets = {
            'path': forms.Textarea,
            'tags': forms.CheckboxSelectMultiple
        }


@admin.register(DataCube)
class DataCubeAdmin(admin.ModelAdmin):
    form = DataCubeAdminForm
    list_display = ['filename', 'path', 'size']
    search_fields = ['filename']
