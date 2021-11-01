from django.db.models import Prefetch
from django.forms import model_to_dict
from django.shortcuts import render

from frontend.forms import create_download_form
from observations.models import DataCube, Observation


def observation_detail(request, observation_pk):
    data_cubes_queryset = DataCube.objects.select_related('previews', 'metadata', 'r0data',
                                                          'spectral_line_data', 'video_preview')
    observation = Observation.objects.prefetch_related(
        Prefetch('cubes', queryset=data_cubes_queryset)).get(pk=observation_pk)

    data_cubes = observation.cubes.all()
    data_cube_count = observation.cubes.count()
    primary_cube = data_cubes[0]

    metadata = primary_cube.metadata

    metadata_fields = {field.verbose_name: field.value_from_object(metadata) for field in metadata._meta.get_fields()}

    # FIXME(daniel): We shouldn't need to pop these from the fields.
    metadata_fields.pop('fits header', None)
    metadata_fields.pop('ID', None)
    metadata_fields.pop('data location', None)
    metadata_fields.pop('data cube', None)
    metadata_fields.pop('Observation ID', None)

    r0_json_data = None
    if hasattr(primary_cube, 'r0data'):
        r0_json_data = primary_cube.r0data.data_json

    spectral_line_data = None
    if hasattr(primary_cube, 'spectral_line_data'):
        spectral_line_data = primary_cube.spectral_line_data.data_json

    download_choices = [(cube.filename, cube.filename) for cube in data_cubes]

    download_form = create_download_form(download_choices)
    download_form.full_clean()

    context = {
        'observation': observation,
        'data_cube_count': data_cube_count,
        'data_cubes': data_cubes,
        'data_cube': primary_cube,
        'download_form': download_form,
        'metadata': metadata,
        'metadata_dict': model_to_dict(metadata),
        'metadata_fields': metadata_fields,
        'r0_json_data': r0_json_data,
        'spectral_line_data': spectral_line_data,
    }

    return render(request, 'frontend/observation_detail.html', context)
