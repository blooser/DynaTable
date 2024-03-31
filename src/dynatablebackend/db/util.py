from sqlalchemy import Double, String, Boolean


table_classes = {}


def str_to_column_type(type_str):
    return {"string": String, "boolean": Boolean, "number": Double}[type_str]


class DynamicRow(object):
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])


def create_table_class(table_id):
    table_type = type(table_id, (DynamicRow,), {})

    table_classes[table_id] = table_type

    return table_type


def get_table_class(table_id):
    if table_id in table_classes:
        return table_classes[table_id]

    return None
