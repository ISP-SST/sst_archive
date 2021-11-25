from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.serializers import DataCubeSerializer
from ingestion.api.data_cube_ingestion_serializer import DataCubeIngestionSerializer
from observations.models import DataCube


class DataCubeIngestionViewSet(viewsets.GenericViewSet):
    """
    ViewSet ingesting new data into the database. Only supports creating and updating
    DataCubes.
    """
    queryset = DataCube.objects.all().select_related('metadata', 'instrument', 'fits_header').prefetch_related(
        'tags').order_by('id')
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = DataCubeIngestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Move the resulting DataCube into a standard DataCube serializer. This is not optimal,
        # but it allows us to work around the asymmetry in the ingestion phase (the amount of
        # information to perform the ingestion is much smaller than the resulting
        # DataCube instances).
        cube_serializer = DataCubeSerializer(serializer.instance)
        headers = self.get_success_headers(cube_serializer.data)
        return Response(cube_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
