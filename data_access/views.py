import os
from urllib.parse import quote_plus

from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from data_access.utils import data_location_requires_login, has_access_to_data_location
from dataset.models import Dataset, DataLocation


def download_data_cube(request: HttpRequest, dataset: str, oid: str) -> HttpResponse:
    # This is where we need to authorize the download.

    # If the metadata specifies that the observation has not yet been released to the public
    # the user needs to have access. The following steps need to be taken:

    # 1. Check if the user is logged in. If not, redirect to a login page that will later bounce
    #    the user back to this view after successful login.
    # 2. Assuming the user was successully logged in, check if the user has permission to
    #    download this cube. In practice this probably means that the user needs to have
    #    a cube-specific permission set on either the user itself, or a group of which the
    #    user is a member.

    dataset_obj = Dataset.objects.get(name__iexact=dataset)
    metadata = dataset_obj.metadata_model.objects.get(oid=oid)
    location: DataLocation = metadata.data_location

    if data_location_requires_login(location):
        if not request.user.is_authenticated:
            # Redirect to login page.
            reversed_login = reverse('login')
            encoded_next = quote_plus(request.get_full_path())

            login_url = '%s?next=%s' % (reversed_login, encoded_next)
            return redirect(login_url)
        else:
            access_granted = request.user.has_perm(
                'data_access.can_access_protected_data') or has_access_to_data_location(request.user, location)

            if not access_granted:
                return render(request, 'data_access/access_denied.html', {
                    'dataset': dataset,
                    'oid': oid,
                    'release_comment': location.access_control.release_comment
                }, status=403)

    path_to_cube = os.path.join(location.file_path, location.file_name)
    if not os.path.exists(path_to_cube):
        return render(request, 'data_access/file_not_found.html', {'filename': location.file_name}, status=404)

    return FileResponse(open(path_to_cube, 'rb'), filename=location.file_name)
