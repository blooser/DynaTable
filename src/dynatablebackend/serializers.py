from rest_framework import serializers


class ColumnSerializer(serializers.Serializer):
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
    child = ColumnSerializer()

    def validate(self, data):
        return data
