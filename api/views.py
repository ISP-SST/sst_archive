from rest_framework import viewsets

from api.serializers import DataCubeSerializer, TagSerializer
from observations.models import DataCube, Tag


class DataCubeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for entire DataCube objects, including nested fields via reverse relations.
    """
    queryset = DataCube.objects.all().select_related('metadata', 'instrument', 'fits_header').prefetch_related(
        'tags').order_by('id')
    serializer_class = DataCubeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
