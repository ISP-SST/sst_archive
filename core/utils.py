import sys

from django.contrib import admin

_MAX_WEIGHT = 1024

_inlines_collection = {}


def extend_admin(root_model_cls, root_admin_cls, new_inline_admin, weight=sys.maxsize):
    inline_tuples = _inlines_collection.get(root_admin_cls, [])

    if not inline_tuples:
        inline_tuples = [(root_admin_cls.inlines[i], i - _MAX_WEIGHT) for i in range(len(root_admin_cls.inlines))]

    inline_tuples.append((new_inline_admin, weight))

    inline_tuples.sort(key=lambda x: x[1])

    new_inlines = [t[0] for t in inline_tuples]

    class AdminAddonClass(root_admin_cls):
        inlines = new_inlines

    admin.site.unregister(root_model_cls)
    admin.site.register(root_model_cls, AdminAddonClass)

    _inlines_collection[root_admin_cls] = inline_tuples
