from django.http import HttpRequest, HttpResponse

from data_access.views import download_data_cube


def download_multiple_data_cubes(request: HttpRequest) -> HttpResponse:
    filename = request.GET.get('files')
    return download_data_cube(request, filename)
