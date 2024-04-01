import pytest
from rest_framework.test import APIClient
from rest_framework import status


from tests.generator import generator


@pytest.fixture
def api_client():
    yield APIClient()


@pytest.mark.django_db
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
def test_create_table(api_client, fields):
    url = "/api/table"

    response = api_client.post(url, fields, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "table_id" in data
    assert isinstance(data["table_id"], str)
    assert len(data["table_id"]) > 0


@pytest.mark.django_db
def test_create_table_validates_data_and_does_not_allow_incorrect_payload(api_client):
    url = "/api/table"
    data = [{"name": "email", "type": "string"}, {"name": "age", "type": "integer"}]

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_table_structure_handle_non_existing_table_id(api_client):
    table_id = "hj40935jh03"

    url = f"/api/table/{table_id}"
    data = [{"name": "phone", "type": "string"}]

    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


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
def test_update_table_structure_does_not_allow_to_update_schema_if_table_contains_rows(
    api_client, fields
):
    url = "/api/table"

    response = api_client.post(url, fields, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "table_id" in data
    assert isinstance(data["table_id"], str)
    assert len(data["table_id"]) > 0

    table_id = data["table_id"]

    url = f"/api/table/{table_id}/row"

    row = fields.row_generator.one()
    response = api_client.post(url, row, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    url = f"/api/table/{table_id}"
    data = generator.model_fields_generator.one()

    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_table_structure_updates_structure(api_client):
    url = "/api/table"
    data = [{"name": "email", "type": "string"}, {"name": "age", "type": "number"}]

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "table_id" in data
    assert isinstance(data["table_id"], str)
    assert len(data["table_id"]) > 0

    table_id = data["table_id"]

    url = f"/api/table/{table_id}"
    data = [{"name": "phone", "type": "string"}]

    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


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
def test_update_table_structure_updates_structure_and_allows_to_put_row(
    api_client, fields
):
    url = "/api/table"

    response = api_client.post(url, fields, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "table_id" in data
    assert isinstance(data["table_id"], str)
    assert len(data["table_id"]) > 0

    table_id = data["table_id"]

    url = f"/api/table/{table_id}"
    data = [{"name": "phone", "type": "string"}]

    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    row = fields.row_generator.one()
    row["phone"] = "+48123456789"

    url = f"/api/table/{table_id}/row"
    response = api_client.post(url, row, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_add_table_row(api_client):
    url = "/api/table"
    data = [{"name": "email", "type": "string"}, {"name": "age", "type": "number"}]

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    table_id = data["table_id"]

    url = f"/api/table/{table_id}/row"
    data = {"email": "test@gmail.com", "age": 55}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_add_table_row_respect_schema(api_client):
    url = "/api/table"
    data = [{"name": "email", "type": "string"}, {"name": "age", "type": "number"}]

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    table_id = data["table_id"]

    url = f"/api/table/{table_id}/row"
    data = {"email": None, "age": False}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_table_rows(api_client):
    url = "/api/table"
    data = [{"name": "email", "type": "string"}, {"name": "age", "type": "number"}]

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    table_id = data["table_id"]

    url = f"/api/table/{table_id}/row"
    data = {"email": "test@gmail.com", "age": 55}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    url = f"/api/table/{table_id}/rows"
    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "test@gmail.com" == data["rows"][0]["email"]
    assert 55 == data["rows"][0]["age"]
