from sqlalchemy import Double, String, Boolean


def str_to_column_type(type_str):
    return {"string": String, "boolean": Boolean, "number": Double}[type_str]
