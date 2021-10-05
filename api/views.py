from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.complex_filters import get_complex_filter
from api.serializers import DataCubeSerializer, TagSerializer, SearchableDataCubeSerializer
from api.utils import get_models_from_fields
from observations.models import DataCube, Tag


class DataCubeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for entire DataCube objects, including nested fields via reverse relations.
    """
    queryset = DataCube.objects.all().select_related('metadata', 'instrument', 'fits_header').prefetch_related(
        'tags').order_by('id')
    serializer_class = DataCubeSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer


@api_view(['GET'])
def search_data_cubes(request):
    """
    Request can contain any number of instances of two query parameters:

    "?s=<search-expression>" - search data cubes using the provided search expression. The search expression
                               is based on the standard Django lookup format, e.g. 'model__field__iexact=<value>'.
    "?f=<field-name>"        - retrieve the specific field from the search results. When one or more "f" query
                               parameters are provided, only those fields will be returned in the response to the
                               request. Only those fields will be used in the SQL query as well, so limiting the
                               number of fields requested can greatly improve performance.

    TODO(daniel): We can make this into a subclass of GenericAPIView
                  to get some features for free, like pagination. That
                  might also help us replace the complex filtering with
                  django-filter.

    :param request:
    :return:
    """
    data_cubes = DataCube.objects.all()

    search_expressions = request.GET.getlist('s', None)
    if search_expressions:
        search_filters = [get_complex_filter(search_expression) for search_expression in search_expressions]
        data_cubes = data_cubes.filter(*search_filters)

    fields = request.GET.getlist('f', None)
    if fields:
        data_cubes = data_cubes.select_related(*get_models_from_fields(fields)).only(*fields)

    serializer = SearchableDataCubeSerializer(data_cubes, fields=fields, many=True)
    return Response(serializer.data)
