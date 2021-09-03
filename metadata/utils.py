"""
from django.http import QueryDict
from tastypie.exceptions import NotRegistered

from api import svo_api

__all__ = ['get_metadata_queryset']


def get_metadata_queryset(metadata_model, query_string='', user=None):
    '''Return a QuerySet of the metadata corresponding to the dataset and query string'''

    # Use the obj_get_list method from the corresponding metadata resource of the dataset to re-create the query set
    # If no metadata resource corresponds to the dataset, return an empty queryset
    try:
        metadata_resource = svo_api.canonical_resource_for(metadata_model)
    except NotRegistered:
        return metadata_model.objects.none()

    # Tastypie ModelResource.obj_get_list method requires a bundle as argument
    # the build_bundle method of the resource creates an empty HttpRequest
    # the GET of the request must be set to a query dict for the filtering of the metadata
    # the user of the request must be set to check for the authorization
    bundle = metadata_resource.build_bundle()
    bundle.request.user = user
    bundle.request.GET = QueryDict(query_string)
    return metadata_resource.obj_get_list(bundle).order_by()
"""
