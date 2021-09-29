from django.http import HttpResponse

from data_access.utils import schedule_archiving_of_files
from dataset.models import DataLocation
from frontend.file_selection import load_selections


def download_selected_data(request):
    selection_list = load_selections(request)

    ROOT_DIR = '/Users/dani2978/local_science_data'
    files = []

    file_list = list(map(lambda selection: selection.filename, selection_list))

    file_info_query = DataLocation.objects.filter(file_name__in=file_list).values_list(
        'data_location__file_path', 'data_location__file_name', 'data_location__file_size').iterator()
    files += [os.path.relpath(os.path.join(file_info[0], file_info[1]), ROOT_DIR) for file_info in file_info_query]

    id = schedule_archiving_of_files(ROOT_DIR, files)
    return HttpResponse(str(id), status=200)
