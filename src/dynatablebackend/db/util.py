from django.db import models

dynamic_models = {}

COLUMN_TYPES = {
    "string": models.CharField(max_length=128),
    "boolean": models.BooleanField(),
    "number": models.FloatField(),
}


class Meta:
    pass


def to_model_types(columns):
    model_types = {
        "__module__": "dynatablebackend",
        "id": models.AutoField(primary_key=True),
    }

    for column in columns:
        model_types[column["name"]] = COLUMN_TYPES[column["type"]]

    return model_types


def create_dynamic_model(table_id, fields):
    attrs = {"__module__": "dynatablebackend", **fields}

    print(fields)

    DynamicModel = type(table_id, (models.Model,), attrs)

    dynamic_models[table_id] = DynamicModel

    return DynamicModel


def get_dynamic_model(table_id):
    if table_id in dynamic_models:
        return dynamic_models[table_id]

    return None


def obj_to_dict(obj):
    return {field.name: getattr(obj, field.name) for field in obj._meta.fields}
