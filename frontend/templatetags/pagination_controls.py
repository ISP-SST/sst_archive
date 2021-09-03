from django import template

register = template.Library()


@register.inclusion_tag('frontend/pagination_controls.html')
def pagination_controls(paginator, page_obj):
    return {'paginator': paginator, 'page_obj': page_obj}