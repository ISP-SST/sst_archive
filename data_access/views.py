import os

from django.http import HttpRequest, HttpResponse, Http404, FileResponse
from django.shortcuts import redirect

from data_access.utils import data_location_requires_login, has_access_to_data_location
from dataset.models import Dataset


def download_data_cube(request: HttpRequest, dataset, oid) -> HttpResponse:
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
    location = metadata.data_location

    if data_location_requires_login(location):
        if not request.user.is_authenticated():
            # Redirect to login page.
            return redirect('login')
        else:
            if not has_access_to_data_location(request.user, location):
                return redirect('access_denied')

    path_to_cube = os.path.join(location.file_path, location.file_name)
    if not os.path.exists(path_to_cube):
        raise Http404('"%s" does not exist at the expected location' % location.file_name)

    return FileResponse(open(path_to_cube, 'rb'), filename=location.file_name)
