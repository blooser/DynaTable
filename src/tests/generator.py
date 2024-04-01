"""
This module provides functionality for generating dummy data for testing purposes.

It defines a class '_generator' which acts as a container for various data generators,
leveraging the 'Generator' class concept. These generators are designed to produce
randomized data that mimics real-world structures and values, aiding in robust and
effective testing scenarios.

The module uses data from 'data.json', a file containing a collection of pre-defined,
structured data that serves as a basis for the generation process. This allows for
consistent and realistic dummy data creation across different instances and usages.

Included Generators:
    - ModelFieldsGenerator: Generates random model fields based on data specifications
      in 'data.json', useful for creating dynamic models.

Usage:
    >> from this_module import generator
    >> model_fields = generator.model_fields_generator.many(n=8)
    # Generates 8 sets of model fields.
    >> model_fields = generator.model_fields_generator.one()
    # Generates 1 set of model fields

Note:
    This module is particularly useful in testing environments where mock data closely
    resembling production data is required but without the need for actual database
    dependencies or network calls.
"""

__version__ = "0.0.1"
__author__ = "Mateusz Solnica (blooser@protonmail.com)"


import json
import pathlib
import random
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
    """
    Loads and returns data from a JSON file for testing purposes.

    This function reads data from 'data.json', which contains dummy data used for testing. The data is loaded
    from a JSON file located in the 'src/tests' directory relative to this script's location. The results are
    cached using lru_cache to improve performance by storing up to 64 of the most recent calls.

    Returns:
        dict or list: The data loaded from the 'data.json' file. The type of data returned (dictionary or list)
                      depends on the structure of the JSON file.

    Note:
        - This function uses functools.lru_cache to cache the results of the function calls. This cache stores
          up to 64 of the most recent unique calls to this function.
        - The 'data.json' file is expected to exist in the 'src/tests' directory.

    Example:
        data = _load()
        # data now contains the contents of 'data.json' file.
    """
    with open(
        f"{pathlib.Path('__file__').resolve().parent}/src/tests/data.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

        return data


class Generator:
    """
    Abstract class for a data generator to produce dummy data for testing.

    This class serves as a base for specific data generators. It leverages a collection of
    data loaded from 'data.json' and provides methods to generate random and multiple instances
    of data. The 'generate' method is intended to be overridden in derived classes to provide
    specific data generation logic.

    Methods:
        random(name): Retrieves a random item from the loaded data based on a specified category.
        one(): Generates a single instance of data using the 'generate' method.
        many(n): Generates 'n' instances of data.
        generate(): Abstract method to be implemented in derived classes for specific data generation.

    Note:
        - Users deriving from this class need to define the 'generate' method to specify how data is generated.
        - The data is loaded from 'data.json' using a helper function '_load'.

    Example:
        class SpecificGenerator(Generator):
            def generate(self):
                # Implement specific generation logic here
    """

    def __init__(self):
        self.data = _load()

    def random(self, name: str):
        return random.choice(self.data[name])

    def one(self):
        return self.generate()

    def many(self, n: int = 5):
        return [self.one() for _ in range(n)]

    def generate(self):
        raise NotImplementedError("Subclasses must implement this method")


class GeneratedModelFields(list):
    """
    A class derived from 'list' that represents generated model fields.

    This class extends the functionality of a list to specifically handle generated model fields.
    Each item in this list is a dictionary representing a model field with its name and type.

    Properties:
        row_generator: A property that returns an instance of ModelRowGenerator.

    Args:
        d (list of dict): A list of dictionaries where each dictionary represents a model field.
    """

    def __init__(self, d):
        super().__init__(d)

    @property
    def row_generator(self):
        """
        Returns a ModelRowGenerator instance for generating rows matching the model fields.
        """
        return ModelRowGenerator(self)


class ModelFieldsGenerator(Generator):
    """
    Generates random model fields for creating dynamic models.

    This class is a specialized generator that produces random fields suitable for creating dynamic models.
    The generated fields are instances of GeneratedModelFields.

    Methods:
        many(n): Generates a specified number of unique model fields.

    Overrides:
        generate(): Generates a single instance of GeneratedModelFields.
    """

    def many(self, n: int = 5):
        """
        Generates a list of unique model fields.

        Args:
            n (int): The number of unique model fields to generate.

        Returns:
            GeneratedModelFields: A list of unique model fields.
        """
        return _remove_duplicates([self.one() for _ in range(n)], key="name")

    def generate(self):
        """
        Generates random model fields.

        Returns:
            GeneratedModelFields: A set of randomly generated model fields, each represented as a dictionary.
        """
        return GeneratedModelFields(
            [
                {"name": self.random("field_name"), "type": self.random("field_type")}
                for _ in range(random.randint(3, 7))
            ]
        )


class ModelRowGenerator(Generator):
    """
    Generates a random row of data that matches the generated model fields.

    This class takes generated model fields and produces a row of data with values
    corresponding to each field's type. It's designed to work with the GeneratedModelFields class.

    Args:
        generated_model (GeneratedModelFields): The generated model fields to base the row generation on.

    Overrides:
        generate(): Generates a single row of data corresponding to the model fields.
    """

    def __init__(self, generated_model: GeneratedModelFields):
        super().__init__()
        self.generated_model = generated_model

    def random_type_value(self, field_type: str):
        """
        Generates a random value based on the field type.

        Args:
            field_type (str): The type of the field for which to generate a value.

        Returns:
            Any: A random value appropriate for the given field type.
        """
        return {
            "string": self.random("name"),
            "number": random.randint(1, 100),
            "boolean": random.choice([True, False]),
        }[field_type]

    def generate(self):
        """
        Generates a random row of data matching the model fields.

        Returns:
            dict: A dictionary representing a row of data, with keys as field names and values as random data.
        """
        return {
            field["name"]: self.random_type_value(field["type"])
            for field in self.generated_model
        }


class _generator:
    """
    A wrapper class for various data generators.

    This class serves as a container for different types of data generators.
    It provides easy access to various generators needed throughout the application.
    Currently, it includes a model fields generator.

    Attributes:
        model_fields_generator (ModelFieldsGenerator): An instance of ModelFieldsGenerator
                                                       used to generate random model fields.
    """

    model_fields_generator = ModelFieldsGenerator()


# Instance of the _generator class
generator = _generator()
