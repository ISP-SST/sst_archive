

def get_models_from_fields(fields):
    """
    Returns a list of models that are referred to by nesting in the
    input. Any fields that belong immediately to the target object
    will be filtered out, and any fields belonging to a nested object
    will be reduced to an entry with the nested field.

    Example:

            input_fields = ['name', 'description', 'nested_field__value', 'nested_field__unit']
            output_fields = get_models_from_fields(input_fields)

            output_fields: ['nested_field']
    """
    models = ['__'.join(f.split('__')[:-1]) for f in fields]
    # TODO(daniel): This can likely be simplified.
    return filter(lambda model: model != '', models)


def get_immediate_fields(fields):
    """
    From a list of fields or filters, return the fields that belong
    directly to the target object. Any deeply nested fields will be
    reduced to the name of the field on the target object that
    constitutes the start of the nesting.

    Example:

        input_fields = ['name', 'description', 'nested_field__value', 'nested_field__unit']
        output_fields = get_immediate_fields(input_fields)

        output_fields: ['name', 'description', 'nested_field']
    """
    return list(set([f.split('__')[0] for f in fields]))


def get_only_nested_fields(parent_field_name, fields):
    """
    Returns a list of all the fields in the provided field list that
    belong to the specified parent field name.

    Example:

        input_fields = ['name', 'description', 'nested_field__value', 'nested_field__unit']
        output_fields = get_only_nested_fields('nested_field', input_fields)

        output_fields: ['value', 'unit']
    """
    prefix = '%s__' % parent_field_name
    return [field.removeprefix(prefix) for field in fields if field.startswith(prefix)]
