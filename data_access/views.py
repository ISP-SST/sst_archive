import os

from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render

from data_access.forms import TokenForm
from data_access.utils import data_cube_requires_access_grant, has_access_to_data_cube, \
    has_valid_token_for_data_cube
from observations.models import DataCube


def download_data_cube(request: HttpRequest, filename: str) -> HttpResponse:
    """View that lets the user download a datacube if they have the right access token or user permissions."""
    data_cube = DataCube.objects.get(filename__iexact=filename)

    form = TokenForm()

    token = None
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid() and form.cleaned_data and 'token' in form.cleaned_data:
            token = form.cleaned_data.get('token')

    access_granted = False
    if data_cube_requires_access_grant(data_cube):
        if token:
            if has_valid_token_for_data_cube(data_cube, token):
                access_granted = True
            else:
                form.add_error('token', 'The specified token is not valid for the selected data cube.')
        elif request.user.is_authenticated:
            access_granted = request.user.has_perm(
                'data_access.can_access_protected_data') or has_access_to_data_cube(request.user, data_cube)
    else:
        access_granted = True

    if not access_granted:
        return render(request, 'data_access/token_prompt.html', {
            'data_cube': data_cube,
            'form': form,
            'release_comment': data_cube.access_control.release_comment
        }, status=403)

    if not os.path.exists(data_cube.path):
        return render(request, 'data_access/file_not_found.html', {'filename': data_cube.filename}, status=404)

    return FileResponse(open(data_cube.path, 'rb'), filename=data_cube.filename)


def download_multiple_data_cubes(request: HttpRequest) -> HttpResponse:
    filename = request.GET.get('files')
    return download_data_cube(request, filename)
