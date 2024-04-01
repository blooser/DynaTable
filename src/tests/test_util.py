import random

import pytest
import shortuuid
from django.db import models
from dynatablebackend.db import util

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
def test_to_model_types_converts_str_to_models_type(fields):
    model_types = util.to_model_types(fields)

    assert model_types["__module__"] == "dynatablebackend"
    assert isinstance(model_types["id"], models.AutoField)

    for field in fields:
        assert field["name"] in model_types

        if field["type"] == "string":
            assert isinstance(model_types[field["name"]], models.CharField)
        elif field["type"] == "boolean":
            assert isinstance(model_types[field["name"]], models.BooleanField)
        elif field["type"] == "number":
            assert isinstance(model_types[field["name"]], models.FloatField)


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
def test_create_dynamic_model_creates_dynamic_model(fields):
    table_id = shortuuid.uuid()

    model_types = util.to_model_types(fields)

    DynamicModel = util.create_dynamic_model(table_id, model_types)

    assert issubclass(DynamicModel, models.Model)

    dir_dynamic_model = dir(DynamicModel)

    assert "__module__" in dir_dynamic_model

    assert DynamicModel.__dict__["__module__"] == "dynatablebackend"


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
def test_get_dynamic_model_returns_dynamic_model(fields):
    table_id = shortuuid.uuid()

    model_types = util.to_model_types(fields)

    DynamicModel1 = util.create_dynamic_model(table_id, model_types)

    DynamicModel2 = util.get_dynamic_model(table_id)

    assert DynamicModel1 is DynamicModel2


def test_get_dynamic_model_returns_none_if_model_not_exists():
    table_id = shortuuid.uuid()
    DynamicModel = util.get_dynamic_model(table_id)

    assert DynamicModel is None


@pytest.mark.parametrize(
    "fields",
    [
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
    ],
)
def test_get_combined_fields_returns_combined_fields(fields):
    table_id = shortuuid.uuid()

    model_types = util.to_model_types(fields)

    util.create_dynamic_model(table_id, model_types)

    new_fields = [{"name": "phone", "type": "string"}]

    combined_fields = util.get_combined_fields(table_id, new_fields)

    assert (
        len(combined_fields) == len(fields) + len(new_fields) + 2
    )  # 2 = __module__ + id

    random_field = random.choice(fields)
    assert random_field["name"] in combined_fields
    assert isinstance(combined_fields["phone"], models.CharField)
