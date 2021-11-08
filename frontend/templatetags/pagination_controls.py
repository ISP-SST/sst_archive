from django import template

register = template.Library()


@register.simple_tag
def replace_query_param(request, field, value):
    params = request.GET.copy()
    params[field] = value
    return params.urlencode()


@register.inclusion_tag('frontend/pagination_controls.html')
def pagination_controls(request, paginator, page_obj):
    return {'request': request, 'paginator': paginator, 'page_obj': page_obj}