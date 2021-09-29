from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.complex_filters import get_complex_filter
from api.serializers import DataCubeSerializer
from api.utils import get_models_from_fields
from observations.models import DataCube


class DataLocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for entire DataLocation objects (including
    nested fields via reverse relations.
    """
    queryset = DataCube.objects.all().select_related('metadata')
    serializer_class = DataCubeSerializer


# TODO(daniel): We can make this into a subclass of GenericAPIView
#               to get some features for free, like pagination. That
#               might also help us replace the complex filtering with
#               django-filter.
@api_view(['GET'])
def search_data_cubes(request):
    data_cubes = DataCube.objects.all()

    search_expressions = request.GET.getlist('s', None)
    if search_expressions:
        search_filters = [get_complex_filter(search_expression) for search_expression in search_expressions]
        data_cubes = data_cubes.filter(*search_filters)

    fields = request.GET.getlist('f', None)
    if fields:
        data_cubes = data_cubes.select_related(*get_models_from_fields(fields)).only(*fields)

    serializer = DataCubeSerializer(data_cubes, fields=fields, many=True)
    return Response(serializer.data)
