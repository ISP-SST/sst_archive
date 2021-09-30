from django import template

register = template.Library()


@register.inclusion_tag('frontend/column_value.html')
def format_column_value(value):
    array_value = value if isinstance(value, list) else None
    value = value if not array_value else None
    return {'value': value, 'array_value': array_value}
