from django.db import models

dynamic_models = {}

MODEL_TYPES = {
    "string": models.CharField,
    "boolean": models.BooleanField,
    "number": models.FloatField,
}


def to_model_types(columns):
    model_types = {
        "__module__": "dynatablebackend",
        "id": models.AutoField(primary_key=True),
    }

    for column in columns:
        model_types[column["name"]] = MODEL_TYPES[
            column["type"]
        ]()  # NOTE: Need this because of binding model problem, ext.

    return model_types


def create_dynamic_model(table_id, fields):
    attrs = {"__module__": __name__, **fields}

    DynamicModel = type(table_id, (models.Model,), attrs)

    dynamic_models[table_id] = DynamicModel

    return DynamicModel


def get_combined_fields(table_id, fields):
    DynamicModel = get_dynamic_model(table_id)

    if DynamicModel is None:
        return None

    model_types = to_model_types(fields)

    for field in DynamicModel._meta.get_fields():
        if field.name not in model_types:
            model_types[field.name] = type(field)()

    return model_types


def get_dynamic_model(table_id):
    if table_id in dynamic_models:
        return dynamic_models[table_id]

    return None


def get_dynamic_models():
    return list(dynamic_models.values())


def obj_to_dict(obj):
    return {field.name: getattr(obj, field.name) for field in obj._meta.fields}
