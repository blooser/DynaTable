from rest_framework import serializers


class ColumnSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=["string", "number", "bool"])

    def validate_type(self, value):
        if value not in ["string", "number", "bool"]:
            raise serializers.ValidationError(
                "Type must be 'string', 'number', or 'bool'."
            )

        return value

    def validate(self, attrs):
        return attrs


class ColumnListSerializer(serializers.ListSerializer):
    child = ColumnSerializer()

    def validate(self, data):
        return data
