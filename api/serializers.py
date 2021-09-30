from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs

from metadata.models import Metadata
from api.utils import get_only_nested_fields, get_immediate_fields
from observations.models import DataCube, Instrument


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be serialized.

    This class was based on an example in the official documentation:
    https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    Modifications were made to allow further filtering in nested
    fields as well. This means that we can do something like this:

    class MySerializer(DynamicFieldsModelSerializer):
        class Meta:
            model = MyModel
            fields = ['name', 'description', 'nested_field']

    serializer = MySerializer(fields=['name', 'nested_field__name_of_nested_field'])
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        self.allowed_fields = fields

        if fields is not None:
            immediate_fields = get_immediate_fields(fields)

            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(immediate_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.

        This override ensures that the allowed fields passed to the
        constructor of the DynamicFieldsModelSerializer are also passed
        on to any nested fields.
        """
        allowed_fields = self.allowed_fields or None

        if allowed_fields:
            allowed_nested_fields = get_only_nested_fields(field_name, allowed_fields)
        else:
            allowed_nested_fields = '__all__'

        class NestedSerializer(DynamicFieldsModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = allowed_nested_fields

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs


class InstrumentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Instrument
        exclude = ['id', 'metadata_content_type']


class MetadataSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Metadata
        exclude = ['id', 'data_cube']


class DataCubeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DataCube
        # Note that any field based on a reverse relation MUST be explicitly
        # specified in this list of fields. If not, the serializer
        # will not serialize that field..
        fields = ['id', 'filename', 'path', 'size', 'metadata', 'instrument']
        depth = 1
