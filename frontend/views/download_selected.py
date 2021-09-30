import os

from django.http import HttpResponse

from data_access.utils import schedule_archiving_of_files
from frontend.file_selection import load_selections
from observations.models import DataCube


def download_selected_data(request):
    selection_list = load_selections(request)

    ROOT_DIR = '/Users/dani2978/local_science_data'
    files = []

    file_list = list(map(lambda selection: selection.filename, selection_list))

    file_info_query = DataCube.objects.filter(filename__in=file_list).values_list(
        'data_cube__path', 'data_cube__size').iterator()
    files += [os.path.relpath(file_info[0], ROOT_DIR) for file_info in file_info_query]

    id = schedule_archiving_of_files(ROOT_DIR, files)
    return HttpResponse(str(id), status=200)
