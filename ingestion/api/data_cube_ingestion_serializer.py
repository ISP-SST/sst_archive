from pathlib import Path

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from data_access.utils import generate_absolute_path_to_data_cube
from ingestion.ingesters.ingest_data_cube import ingest_data_cube


class DataCubeIngestionSerializer(serializers.Serializer):
    """
    This serializer is responsible for the mechanics of taking a description of a new data cube and
    ingesting it into the database.
    """
    oid = serializers.CharField(required=False)
    relative_path = serializers.CharField()

    owner_email_addresses = serializers.ListField(required=False)
    swedish_data = serializers.BooleanField(required=False)

    def validate_relative_path(self, value):
        path = Path(generate_absolute_path_to_data_cube(value))

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
        oid = data_cube_data.get('oid', None)
        fits_path = generate_absolute_path_to_data_cube(data_cube_data['relative_path'])

        owner_email_addresses = data_cube_data.get('owner_email_addresses', None)
        swedish_data = data_cube_data.get('swedish_data', None)

        try:
            ingested_cube = ingest_data_cube(fits_path,
                                             generate_image_previews=True,
                                             generate_video_previews=True,
                                             owner_email_addresses=owner_email_addresses,
                                             swedish_data=swedish_data,
                                             oid=oid)
        except Exception as e:
            raise ValidationError(e)

        return ingested_cube
