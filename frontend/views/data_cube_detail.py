from django.forms import model_to_dict
from django.shortcuts import render

from observations.models import DataCube


def data_cube_detail(request, filename):
    data_cube = DataCube.objects.select_related('animated_preview', 'thumbnail', 'metadata').get(
        filename__iexact=filename)
    metadata = data_cube.metadata

    metadata_fields = {field.verbose_name: field.value_from_object(metadata) for field in metadata._meta.get_fields()}

    # FIXME(daniel): We shouldn't need to pop these from the fields.
    metadata_fields.pop('fits header', None)
    metadata_fields.pop('ID', None)
    metadata_fields.pop('data location', None)
    metadata_fields.pop('data cube', None)
    metadata_fields.pop('Observation ID', None)

    context = {
        'data_cube': data_cube,
        'metadata': metadata,
        'metadata_dict': model_to_dict(metadata),
        'metadata_fields': metadata_fields,
    }

    return render(request, 'frontend/data_cube_detail.html', context)
