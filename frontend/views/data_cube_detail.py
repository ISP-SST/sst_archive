from django.forms import model_to_dict
from django.shortcuts import render

from observations.models import DataCube


def data_cube_detail(request, filename):
    data_cube = DataCube.objects.select_related('animated_preview', 'previews', 'metadata', 'r0data',
                                                'spectral_line_data', 'video_preview').get(
        filename__iexact=filename)
    metadata = data_cube.metadata

    metadata_fields = {field.verbose_name: field.value_from_object(metadata) for field in metadata._meta.get_fields()}

    # FIXME(daniel): We shouldn't need to pop these from the fields.
    metadata_fields.pop('fits header', None)
    metadata_fields.pop('ID', None)
    metadata_fields.pop('data location', None)
    metadata_fields.pop('data cube', None)
    metadata_fields.pop('Observation ID', None)

    r0_json_data = None
    r0_json_version = None
    if hasattr(data_cube, 'r0data'):
        r0_json_data = data_cube.r0data.data_json
        r0_json_version = data_cube.r0data.data_version

    spectral_line_data = None
    spectral_line_data_version = None
    if hasattr(data_cube, 'spectral_line_data'):
        spectral_line_data = data_cube.spectral_line_data.data_json
        spectral_line_data_version = data_cube.spectral_line_data.data_version

    context = {
        'data_cube': data_cube,
        'metadata': metadata,
        'metadata_dict': model_to_dict(metadata),
        'metadata_fields': metadata_fields,
        'r0_json_data': r0_json_data,
        'r0_json_version': r0_json_version,
        'spectral_line_data': spectral_line_data,
        'spectral_line_data_version': spectral_line_data_version
    }

    return render(request, 'frontend/data_cube_detail.html', context)
