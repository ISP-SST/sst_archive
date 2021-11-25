import os
from pathlib import Path

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ingestion.ingesters.ingest_data_cube import ingest_data_cube


def _generate_absolute_path_to_data_cube(relative_path):
    # Do not allow navigation upwards in the directory tree.
    relative_path = relative_path.replace('..', '')
    return os.path.join(settings.SCIENCE_DATA_ROOT, relative_path)


class DataCubeIngestionSerializer(serializers.Serializer):
    """
    This serializer is responsible for the mechanics of taking a description of a new data cube and
    ingesting it into the database.
    """
    oid = serializers.CharField()
    relative_path = serializers.CharField()

    owner_email_addresses = serializers.ListField()
    swedish_data = serializers.BooleanField()

    def validate_relative_path(self, value):
        path = Path(_generate_absolute_path_to_data_cube(value))

        if not path.is_file():
            raise ValidationError(
                'File pointed to by path does not exist, is not a file, or is not accessible from the host of '
                'this service')

        if path.suffix != '.fits':
            raise ValidationError('File does not carry the expected .fits extension')

        return value

    def create(self, validated_data):
        """
        Create a new DataCube for ingestion.
        """
        data_cube = self.ingest(validated_data)
        return data_cube

    def update(self, data_cube, validated_data):
        """
        Update an already ingested DataCube.
        """
        self.ingest(validated_data)
        return data_cube

    def ingest(self, data_cube_data):
        oid = data_cube_data['oid']
        fits_path = _generate_absolute_path_to_data_cube(data_cube_data['relative_path'])

        owner_email_addresses = data_cube_data['owner_email_addresses']
        swedish_data = data_cube_data['swedish_data']

        try:
            ingested_cube = ingest_data_cube(oid, fits_path,
                                             generate_image_previews=True,
                                             generate_video_previews=True,
                                             owner_email_addresses=owner_email_addresses,
                                             swedish_data=swedish_data)
        except Exception as e:
            raise ValidationError(e)

        return ingested_cube