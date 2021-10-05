from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser

from .serializers.data_cube_ingestion_serializer import DataCubeIngestionSerializer
from observations.models import DataCube


class DataCubeIngestionViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet ingesting new data into the database. Only supports creating and updating
    DataCubes.
    """
    queryset = DataCube.objects.all().select_related('metadata', 'instrument', 'fits_header').prefetch_related('tags').order_by('id')
    serializer_class = DataCubeIngestionSerializer
    permission_classes = [IsAdminUser]
