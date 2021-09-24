from django.contrib import admin

from dataset.admin import DataLocationAdmin
from dataset.models import DataLocation
from tags.models import DataLocationTag, TagCategory, Tag


class TagInline(admin.StackedInline):
    model = Tag


@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]


@admin.register(DataLocationTag)
class DataLocationTagAdmin(admin.ModelAdmin):
    search_fields = ['data_location__file_name']


class DataLocationTagInline(admin.StackedInline):
    model = DataLocationTag
    fk_name = "data_location"


# FIXME(daniel): Would be nice if we can achieve a nicer modularization of the DataLocation admin page.
#                In order to inline the editing of other models from an admin page we currently need to patch
#                the original DataLocationAdmin object. This doesn't scale if more apps would like to add
#                their models to the same admin page.
class MyDataLocationAdmin(DataLocationAdmin):
    inlines = [
        DataLocationTagInline,
    ]

admin.site.unregister(DataLocation)
admin.site.register(DataLocation, MyDataLocationAdmin)
