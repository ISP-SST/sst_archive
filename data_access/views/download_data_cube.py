import os

from django.conf import settings
from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render

from data_access.models import is_data_cube_restricted_to_swedish_users
from data_access.utils import data_cube_requires_access_grant, has_valid_token_for_data_cube, user_has_access_to_data_cube
from observations.models import DataCube


def download_data_cube(request: HttpRequest, filename: str) -> HttpResponse:
    """
    View that lets the user download a DataCube if they have the right access token or user permissions.
    """
    data_cube = DataCube.objects.get(filename__iexact=filename)

    access_granted = False
    if data_cube_requires_access_grant(data_cube):
        if request.user.is_authenticated:
            access_granted = request.user.has_perm(
                'data_access.can_access_protected_data') or user_has_access_to_data_cube(request.user, data_cube)
    else:
        access_granted = True

    swedish_data = is_data_cube_restricted_to_swedish_users(data_cube)

    if not access_granted:
        return render(request, 'data_access/access_denied.html', {
            'data_cube': data_cube,
            'admin_email': settings.ADMIN_EMAIL,
            'swedish_data': swedish_data,
            'release_comment': data_cube.access_control.release_comment
        }, status=403)

    if not os.path.exists(data_cube.path):
        return render(request, 'data_access/file_not_found.html', {'filename': data_cube.filename}, status=404)

    return FileResponse(open(data_cube.path, 'rb'), filename=data_cube.filename)
