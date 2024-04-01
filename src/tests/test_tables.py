import pytest
from django.db import connection
from dynatablebackend.db import tables

from tests.generator import generator


def _table_name(table_id: str):
    return f"dynatablebackend_{table_id.lower()}"


@pytest.mark.django_db
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
def test_create_table_creates_table(fields):
    table_id = tables.create_table(fields)

    assert type(table_id) is str
    assert len(table_id) > 0

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = %s)",
            [_table_name(table_id)],
        )
        assert cursor.fetchone()[0]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "fields",
    [
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
        (generator.model_fields_generator.one()),
    ],
)
def test_create_table_creates_table_with_particural_table_id(fields):
    table_id = tables.create_table(fields, "proexe")

    assert table_id == "proexe"
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = %s)",
            [_table_name("proexe")],
        )
        assert cursor.fetchone()[0]


@pytest.mark.django_db
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
def test_add_table_row_adds_table_row(fields):
    table_id = tables.create_table(fields)

    assert isinstance(table_id, str)
    assert len(table_id) > 0

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = %s)",
            [_table_name(table_id)],
        )
        assert cursor.fetchone()[0]

    rows = fields.row_generator.many()

    for row in rows:
        assert tables.add_table_row(table_id, row)

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {_table_name(table_id)}")
        db_rows = cursor.fetchall()

        assert len(db_rows) == len(rows)

        for row, db_row in zip(rows, db_rows):
            for field in row:
                assert row[field] in db_row


@pytest.mark.django_db
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
def test_update_table_updates_tables_schema(fields):
    assert True


@pytest.mark.django_db
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
def test_get_table_rows_returns_table_rows(fields):
    table_id = tables.create_table(fields)

    rows = fields.row_generator.many()

    for row in rows:
        assert tables.add_table_row(table_id, row)

    db_rows = tables.get_table_rows(table_id)

    assert len(rows) == len(db_rows)

    for row, db_row in zip(rows, db_rows):
        for field in row:
            assert row[field] == db_row[field]
