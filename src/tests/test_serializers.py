import pytest
from dynatablebackend.serializers import ColumnListSerializer, ColumnSerializer

from tests.generator import generator


@pytest.mark.parametrize(
    "fields",
    [
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
    ],
)
def test_column_serializer_validates_one_column(fields):
    for field in fields:
        column_serializer = ColumnSerializer(data=field)

        assert column_serializer.is_valid()


def test_column_serializer_detects_errors():
    incorrect_data = {"name": "title", "type": "list"}

    column_serializer = ColumnSerializer(data=incorrect_data)

    assert not column_serializer.is_valid()


@pytest.mark.parametrize(
    "fields",
    [
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
    ],
)
def test_column_slist_serializer_validates_columns(fields):
    column_list_serializer = ColumnListSerializer(data=fields)

    assert column_list_serializer.is_valid()


@pytest.mark.parametrize(
    "fields",
    [
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
    ],
)
def test_column_list_serializer_detects_errors(fields):
    incorrect_data = fields + [{"name": "title", "type": "list"}]

    column_list_serializer = ColumnListSerializer(data=incorrect_data)

    assert not column_list_serializer.is_valid()
