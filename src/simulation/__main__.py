import argparse

import requests
from dynatable.logger import get_logger
from tests.generator import generator

logger = get_logger(__name__)


def _show(data):
    """
    Displays the table ID and its rows in a formatted manner.

    Args:
        data (dict): A dictionary containing 'table_id' and 'rows' of a table.
    """
    table_id = data["table_id"]
    rows = data["rows"]

    print(f"{'=' * 25}\nTable: '{table_id}'\nRows:")

    for row in rows:
        print(f"  {list(row.values())}")

    print("")


def simulate_table(host: str):
    """
    Simulates table creation, row insertion, and data retrieval in DynaTable.

    Args:
        host (str): The URI of the DynaTable backend.

    Returns:
        dict: A dictionary with table ID and the rows inserted into the table.
    """
    # Create a new table
    url = f"{host}/api/table"
    model_fields = generator.model_fields_generator.one()
    response = requests.post(url, json=model_fields)
    table_id = response.json()["table_id"]

    # Insert rows into the table
    url = f"{host}/api/table/{table_id}/row"
    rows_to_insert = model_fields.row_generator.many(5)
    for row in rows_to_insert:
        requests.post(url, json=row)

    # Retrieve rows from the table
    url = f"{host}/api/table/{table_id}/rows"
    response = requests.get(url)
    rows = response.json()["rows"]

    return {"table_id": table_id, "rows": rows}


def main():
    """
    The main function that parses command-line arguments and initiates table simulation.
    """
    parser = argparse.ArgumentParser(
        description="Command-line program for interacting with DynaTable."
    )

    parser.add_argument(
        "-t",
        "--tables",
        type=int,
        choices=range(1, 11),
        help="Number of tables to be created. Accepts an integer from 1 to 10.",
    )

    parser.add_argument(
        "--host", type=str, required=True, help="URI to the host backend Django REST."
    )

    args = parser.parse_args()
    logger.info(f"HOST URI: {args.host}, Number of tables: {args.tables}")

    for _ in range(args.tables):
        result = simulate_table(args.host)
        _show(result)


if __name__ == "__main__":
    main()
