from django.core.exceptions import ObjectDoesNotExist
from pathlib import Path
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from ingestion.utils.ingest_metadata import ingest_metadata, InvalidFITSHeader
from metadata.models import FITSHeader
from observations.models import Instrument, DataCube, Tag


class DataCubeIngestionSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for the mechanics of taking a description of a new data cube and
    ingesting it into the database.
    """

    fits_header = serializers.CharField()
    path = serializers.CharField()

    instrument = PrimaryKeyRelatedField(queryset=Instrument.objects.all())

    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = DataCube
        # Note that any field based on a reverse relation MUST be explicitly specified in this list of fields.
        # If not, the serializer will not serialize that field.
        fields = ['id', 'oid', 'path', 'filename', 'size', 'instrument', 'fits_header', 'tags']
        depth = 1

    def validate_path(self, value):
        path = Path(value)

        if not path.is_file():
            raise ValidationError(
                'File pointed to by path does not exist, is not a file, or is not accessible from the host of this service')

        if path.suffix != '.fits':
            raise ValidationError('File does not carry the expected .fits extension')

        return value

    def create(self, validated_data):
        """
        Create a new DataCube for ingestion.
        """
        fits_header_data = validated_data.pop('fits_header')

        tags_data = validated_data.pop('tags', None)

        data_cube = DataCube.objects.create(**validated_data)

        FITSHeader.objects.create(data_cube=data_cube, fits_header=fits_header_data)

        try:
            ingest_metadata(fits_header_data, data_cube)
        except InvalidFITSHeader as e:
            raise ValidationError(e)

        data_cube.tags.set(tags_data)

        return data_cube

    def update(self, data_cube, validated_data):
        """
        Update an already ingested DataCube.
        """
        fits_header_data = validated_data.pop('fits_header')

        tags = validated_data.pop('tags') or data_cube.tags

        DataCube.objects.filter(id=data_cube.id).update(**validated_data)

        FITSHeader.objects.filter(data_cube=data_cube).update(fits_header=fits_header_data)

        try:
            ingest_metadata(fits_header_data, data_cube)
        except InvalidFITSHeader as e:
            raise ValidationError(e)

        data_cube.tags.set(tags)

        return data_cube
