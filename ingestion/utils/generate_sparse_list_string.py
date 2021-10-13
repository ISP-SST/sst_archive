def _write_elements_to_string(output_string, range_start, range_end):
    if output_string:
        output_string += ','

    if range_start == range_end:
        # Write a single item.
        output_string += '%s' % (str(range_end))
    else:
        # Write a range.
        output_string += '%s-%s' % (str(range_start), str(range_end))

    return output_string


def generate_sparse_list_string(items):
    """
    Assumes a sorted list of items that support addition, comparison and conversion to strings.
    """
    sparse_list_string = ''

    range_start = None
    last_item = None

    for i in items:
        if range_start is None:
            range_start = i

        if last_item is not None and i != last_item + 1:
            sparse_list_string = _write_elements_to_string(sparse_list_string, range_start, last_item)
            range_start = i

        last_item = i

    # Add the last range or single item.
    sparse_list_string = _write_elements_to_string(sparse_list_string, range_start, last_item)

    return sparse_list_string