from django import forms


def add_bootstrap_form_classes_to_fields(fields):
    for field_name in fields:
        field = fields[field_name]
        if isinstance(field.widget, forms.CheckboxInput):
            class_name = 'form-check-input'
        else:
            class_name = 'form-control'

        field.widget.attrs['class'] = class_name
