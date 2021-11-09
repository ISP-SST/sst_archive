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

    is_data_cube_group = data_cube_count > 1

    date_beg = primary_cube.metadata.date_beg
    date_end = primary_cube.metadata.date_end
    instruments = set()
    spectral_lines = set()
    total_number_of_scans = 0

    for cube in data_cubes:
        date_beg = min(date_beg, cube.metadata.date_beg)
        date_end = max(date_end, cube.metadata.date_end)
        instruments.add(cube.instrument.name)
        spectral_lines.add(cube.metadata.waveband)
        total_number_of_scans += cube.metadata.naxis5

    context = {
        'observation': observation,
        'is_data_cube_group': is_data_cube_group,
        'date_beg': date_beg,
        'date_end': date_end,
        'instruments': instruments,
        'spectral_lines': spectral_lines,
        'total_number_of_scans': total_number_of_scans,
        'data_cubes': data_cubes,
        'data_cube': primary_cube,
        'download_form': download_form,
        'metadata': metadata,
        'metadata_fields': metadata_fields,
        'r0_json_data': r0_json_data,
        'spectral_line_data': spectral_line_data,
    }

    return render(request, 'frontend/observation_detail.html', context)
