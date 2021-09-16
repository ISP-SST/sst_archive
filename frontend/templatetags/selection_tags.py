from django import template

register = template.Library()


@register.inclusion_tag('frontend/selection_control.html')
def show_selection_control(filename, selected):
    return {'filename': filename, 'selected': selected}
