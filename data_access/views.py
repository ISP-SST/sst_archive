import os

from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render

from data_access.forms import TokenForm
from data_access.utils import data_location_requires_access_grant, has_access_to_data_location, \
    has_valid_token_for_data_location
from dataset.models import Dataset, DataLocation


def download_data_cube(request: HttpRequest, dataset: str, oid: str) -> HttpResponse:
    """View that lets the user download a datacube if they have the right access token or user permissions."""
    dataset_obj = Dataset.objects.get(name__iexact=dataset)
    metadata = dataset_obj.metadata_model.objects.get(oid=oid)
    data_location: DataLocation = metadata.data_location

    form = TokenForm()

    token = None
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid() and form.cleaned_data and 'token' in form.cleaned_data:
            token = form.cleaned_data.get('token')

    access_granted = False
    if data_location_requires_access_grant(data_location):
        if token:
            if has_valid_token_for_data_location(data_location, token):
                access_granted = True
            else:
                form.add_error('token', 'The specified token is not valid for the selected data cube.')
        elif request.user.is_authenticated:
            access_granted = request.user.has_perm(
                'data_access.can_access_protected_data') or has_access_to_data_location(request.user, data_location)
    else:
        access_granted = True

    if not access_granted:
        return render(request, 'data_access/token_prompt.html', {
            'dataset': dataset,
            'oid': oid,
            'data_location': data_location,
            'form': form,
            'release_comment': data_location.access_control.release_comment
        }, status=403)

    path_to_cube = os.path.join(data_location.file_path, data_location.file_name)
    if not os.path.exists(path_to_cube):
        return render(request, 'data_access/file_not_found.html', {'filename': data_location.file_name}, status=404)

    return FileResponse(open(path_to_cube, 'rb'), filename=data_location.file_name)
