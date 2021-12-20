from django.db.models import Prefetch, Q
from django.shortcuts import render

from data_access.models import are_some_data_cubes_accessible_to_swedish_users
from data_access.utils import data_cube_requires_access_grant
from frontend.forms import create_download_form
from observations.models import DataCube, Observation


def observation_detail(request, observation_pk):
    data_cubes_queryset = DataCube.objects.select_related('instrument', 'previews', 'metadata', 'r0data',
                                                          'spectral_line_data', 'video_preview', 'access_control')
    observation = Observation.objects.prefetch_related(
        Prefetch('cubes', queryset=data_cubes_queryset)).get(pk=observation_pk)

    data_cubes = observation.cubes.all()
    data_cube_count = observation.cubes.count()
    primary_cube = data_cubes[0]

    metadata = primary_cube.metadata
    metadata_fields = metadata.get_metadata_fields()

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
    observers = set()
    polarimetric = False

    restricted = False
    release_date = None
    release_comment = ''

    swedish_data = are_some_data_cubes_accessible_to_swedish_users(data_cubes)

    for cube in data_cubes:
        date_beg = min(date_beg, cube.metadata.date_beg)
        date_end = max(date_end, cube.metadata.date_end)
        instruments.add(cube.instrument.name)
        spectral_lines.add(cube.metadata.waveband)
        observers.add(cube.metadata.observer)
        polarimetric = polarimetric or cube.metadata.naxis4 > 1
        total_number_of_scans += cube.metadata.naxis5

        restricted = restricted or data_cube_requires_access_grant(cube)

        if release_date:
            release_date = min(cube.access_control.release_date, release_date)
        else:
            release_date = cube.access_control.release_date

        release_comment = release_comment or cube.access_control.release_comment

    overlapping_data_cubes = DataCube.objects.exclude(Q(metadata__date_beg__gt=observation.date_end) |
                                                      Q(metadata__date_end__lt=observation.date_beg) |
                                                      Q(pk__in=[cube.id for cube in data_cubes])).select_related(
        'previews', 'metadata', 'instrument', 'observation')

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
        'observers': observers,
        'polarimetric': polarimetric,
        'restricted': restricted,
        'release_date': release_date,
        'swedish_data': swedish_data,
        'release_comment': release_comment,
        'overlapping_data_cubes': overlapping_data_cubes
    }

    return render(request, 'frontend/observation_detail.html', context)
