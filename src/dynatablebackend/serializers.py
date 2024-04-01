from rest_framework import serializers


class ColumnSerializer(serializers.Serializer):
    """
    Serializer for a column definition with validations.

    This serializer defines a column with 'name' and 'type' fields. The 'type' field
    is restricted to specific choices - 'string', 'number', or 'boolean'. It includes
    custom validation to ensure the 'type' field adheres to these choices.

    Attributes:
        name (CharField): A field for the column name with a maximum length of 100.
        type (ChoiceField): A choice field for the column type.

    Methods:
        validate_type(value): Validates that the 'type' field contains a valid choice.
        validate(attrs): Returns the attributes as-is after performing default validation.
    """

    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=["string", "number", "boolean"])

    def validate_type(self, value):
        if value not in ["string", "number", "boolean"]:
            raise serializers.ValidationError(
                "Type must be 'string', 'number', or 'boolean'."
            )
        return value

    def validate(self, attrs):
        return attrs


class ColumnListSerializer(serializers.ListSerializer):
    """
    List serializer for handling a collection of ColumnSerializer instances.

    This serializer is a list serializer that specifically handles multiple instances
    of ColumnSerializer. It is designed to serialize and validate a list of column definitions.

    Attributes:
        child (ColumnSerializer): A serializer for individual column items in the list.

    Methods:
        validate(data): Returns the data as-is after performing default validation.
    """

    child = ColumnSerializer()

    def validate(self, data):
        return data
