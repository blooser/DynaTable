import json
import random
import pathlib
from functools import lru_cache


def _remove_duplicates(dict_list, key):
    """
    Removes duplicates from a list of dictionaries based on a specified key.

    Args:
    dict_list (list): The list of dictionaries from which duplicates are to be removed.
    key (str): The dictionary key to be used for identifying duplicates.

    Returns:
    list: A list of dictionaries without duplicates.
    """
    seen = set()
    return [d for d in dict_list if d[key] not in seen and not seen.add(d[key])]


@lru_cache(maxsize=64)
def _load():
    with open(
        f"{pathlib.Path('__file__').resolve().parent}/src/tests/data.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

        return data


class Generator:
    def __init__(self):
        self.data = _load()

    def random(self, name):
        return random.choice(self.data[name])

    def one(self, rule={}):
        return self.generate(rule)

    def many(self, n=5, rule={}):
        return [self.one(rule) for _ in range(n)]

    def generate(self):
        return NotImplemented


class GeneratedModelFields(list):
    def __init__(self, d):
        super().__init__(d)

    @property
    def row_generator(self):
        return ModelRowGenerator(self)


class ModelFieldsGenerator(Generator):
    def many(self, n=5):
        return _remove_duplicates([self.one() for _ in range(n)], key="name")

    def generate(self, rule={}):
        return GeneratedModelFields(
            [
                {"name": self.random("field_name"), "type": self.random("field_type")}
                for _ in range(random.randint(3, 7))
            ]
        )


class ModelRowGenerator(Generator):
    def __init__(self, generated_model):
        super().__init__()

        self.generated_model = generated_model

    def random_type_value(self, field_type):
        return {
            "string": self.random("name"),
            "number": random.randint(1, 100),
            "boolean": random.choice([True, False]),
        }[field_type]

    def generate(self, rule={}):
        return {
            field["name"]: self.random_type_value(field["type"])
            for field in self.generated_model
        }


class _generator:
    model_fields_generator = ModelFieldsGenerator()


generator = _generator()
