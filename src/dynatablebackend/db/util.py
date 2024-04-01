from django.db import models

# Global dictionary to store dynamic models
dynamic_models = {}

# Only allowed types in dynamic model
MODEL_TYPES = {
    "string": models.CharField,
    "boolean": models.BooleanField,
    "number": models.FloatField,
}


def to_model_types(columns):
    """
    Converts a list of column definitions to Django model field types.

    Each column is transformed into an appropriate Django model field type, based
    on the mapping defined in the MODEL_TYPES dictionary. The function
    automatically adds an 'id' field as an AutoField, serving as the primary key.

    Args:
        columns (list of dict): A list of dictionaries representing columns, where
                                each dictionary contains 'name' (the column name)
                                and 'type' (the type of data, e.g., 'string').

    Returns:
        dict: A dictionary with field names as keys and Django model field types as values.

    Example:
        columns = [{"name": "name", "type": "string"}, {"name": "age", "type": "integer"}]
        to_model_types(columns)
        # Result: {"__module__": "dynatablebackend", "id": AutoField(...), "name": CharField(...), "age": IntegerField(...)}
    """

    model_types = {
        "__module__": "dynatablebackend",
        "id": models.AutoField(primary_key=True),
    }

    for column in columns:
        model_types[column["name"]] = MODEL_TYPES[column["type"]]()

    return model_types


def create_dynamic_model(table_id, fields):
    """
    Dynamically creates a new Django model with the specified fields.

    This function uses Python's type function to create a new model class at runtime.
    It assigns the model to a global dictionary for reference. The model includes
    the given fields and is named using the provided table_id.

    Args:
        table_id (str): The name of the dynamic model (also used as the database table name).
        fields (dict): A dictionary where keys are field names and values are Django model fields.
                       For example, {'name': models.CharField(...), 'age': models.IntegerField(...)}

    Returns:
        class: A new dynamically created Django model class.

    Example:
        fields = {'name': models.CharField(max_length=100), 'age': models.IntegerField()}
        model = create_dynamic_model('Person', fields)
        # 'Person' model is now created with 'name' and 'age' fields.
    """
    attrs = {"__module__": __name__, **fields}

    DynamicModel = type(table_id, (models.Model,), attrs)

    dynamic_models[table_id] = DynamicModel

    return DynamicModel


def get_combined_fields(table_id, fields):
    """
    Combines fields from a provided list with the fields of an existing dynamic model.

    This function retrieves a dynamic model by its table identifier. If the model exists,
    it combines its fields with the new fields provided. If a field from the new fields
    list shares a name with a field from the dynamic model, the new field overrides the
    existing one. If the dynamic model does not exist, the function returns None.

    Args:
        table_id (str): The identifier of the table (model name) whose fields are to be combined.
        fields (list of dict): A list of dictionaries representing new fields to combine, where
                               each dictionary contains 'name' (field name) and 'type' (field data type).

    Returns:
        dict or None: A dictionary of combined field types if the dynamic model exists, otherwise None.

    Example:
        new_fields = [{"name": "title", "type": "string"}, {"name": "description", "type": "text"}]
        combined_fields = get_combined_fields("BlogPost", new_fields)
        # Returns combined fields of 'BlogPost' model and new_fields, with new_fields taking precedence.
    """

    DynamicModel = get_dynamic_model(table_id)

    if DynamicModel is None:
        return None

    model_types = to_model_types(fields)

    for field in DynamicModel._meta.get_fields():
        if field.name not in model_types:
            model_types[field.name] = type(field)()

    return model_types


def get_dynamic_model(table_id):
    """
    Retrieves a dynamically created Django model by its table identifier.

    This function looks up the global dictionary of dynamic models and returns the model
    associated with the given table_id, if it exists. If no model is found with the given
    table_id, the function returns None.

    Args:
        table_id (str): The identifier of the table (model name) to retrieve.

    Returns:
        class or None: The dynamically created Django model class if found, otherwise None.

    Example:
        model = get_dynamic_model('Person')
        # Returns the 'Person' model if it exists, otherwise None.
    """
    if table_id in dynamic_models:
        return dynamic_models[table_id]

    return None


def obj_to_dict(obj):
    return {field.name: getattr(obj, field.name) for field in obj._meta.fields}
