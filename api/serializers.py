from rest_framework import serializers

from metadata.models import Metadata
from observations.models import DataCube, Instrument, Tag


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        exclude = []


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        exclude = ['id', 'data_cube']
        depth = 0


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = []


class InlineInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['name']


class DataCubeSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(required=False)
    instrument = InlineInstrumentSerializer()

    tags = TagSerializer(many=True)

    class Meta:
        model = DataCube
        # Note that any field based on a reverse relation MUST be explicitly
        # specified in this list of fields. If not, the serializer
        # will not serialize that field..
        fields = ['id', 'oid', 'path', 'filename', 'size', 'metadata', 'instrument', 'tags']
        depth = 1
