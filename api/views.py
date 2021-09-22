from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from dataset.models import DataLocation
from api.complex_filters import get_complex_filter
from api.serializers import DataLocationSerializer
from api.utils import get_models_from_fields


class DataLocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for entire DataLocation objects (including
    nested fields via reverse relations.
    """
    queryset = DataLocation.objects.all().select_related('metadata')
    serializer_class = DataLocationSerializer


# TODO(daniel): We can make this into a subclass of GenericAPIView
#               to get some features for free, like pagination. That
#               might also help us replace the complex filtering with
#               django-filter.
@api_view(['GET'])
def search_data_locations(request):
    data_locations = DataLocation.objects.all()

    search_expressions = request.GET.getlist('s', None)
    if search_expressions:
        search_filters = [get_complex_filter(search_expression) for search_expression in search_expressions]
        data_locations = data_locations.filter(*search_filters)

    fields = request.GET.getlist('f', None)
    if fields:
        data_locations = data_locations.select_related(*get_models_from_fields(fields)).only(*fields)

    serializer = DataLocationSerializer(data_locations, fields=fields, many=True)
    return Response(serializer.data)
