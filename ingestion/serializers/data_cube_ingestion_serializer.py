from pathlib import Path

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ingestion.utils.ingest_data_cube import ingest_data_cube
from observations.models import Instrument


class DataCubeIngestionSerializer(serializers.Serializer):
    """
    This serializer is responsible for the mechanics of taking a description of a new data cube and
    ingesting it into the database.
    """
    oid = serializers.CharField()
    path = serializers.CharField()

    instrument = serializers.PrimaryKeyRelatedField(queryset=Instrument.objects.all())

    class Meta:
        depth = 1

    def validate_path(self, value):
        path = Path(value)

        if not path.is_file():
            raise ValidationError(
                'File pointed to by path does not exist, is not a file, or is not accessible from the host of' 
                'this service')

        if path.suffix != '.fits':
            raise ValidationError('File does not carry the expected .fits extension')

        return value

    def create(self, validated_data):
        """
        Create a new DataCube for ingestion.
        """
        data_cube_data = validated_data

        oid = data_cube_data['oid']
        fits_path = data_cube_data['path']
        instrument = data_cube_data['instrument']

        data_cube = ingest_data_cube(oid, fits_path, instrument=instrument)

        return data_cube

    def update(self, data_cube, validated_data):
        """
        Update an already ingested DataCube.
        """
        data_cube_data = validated_data

        oid = data_cube_data['oid']
        fits_path = data_cube_data['path']
        instrument = data_cube_data['instrument']

        ingest_data_cube(oid, fits_path, instrument=instrument)

        return data_cube
