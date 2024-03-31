import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


def test_create_table(api_client):
    url = "/api/table"
    data = [{"name": "email", "type": "string"}, {"name": "age", "type": "number"}]

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "table_id" in data
    assert isinstance(data["table_id"], str)
    assert len(data["table_id"]) > 0


def test_create_table_validates_data_and_does_not_allow_incorrect_payload(api_client):
    url = "/api/table"
    data = [{"name": "email", "type": "string"}, {"name": "age", "type": "integer"}]

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.skip
def test_update_table_structure(api_client):
    url = "/api/table/1"  # Zakładając, że tabela o ID 1 istnieje
    data = {
        # Tu powinny zostać dodane odpowiednie dane
    }
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    # Dodatkowe asercje mogą być tutaj umieszczone


@pytest.mark.skip
def test_add_table_row(api_client):
    url = "/api/table/1/row"  # Zakładając, że tabela o ID 1 istnieje
    data = {
        # Tu powinny zostać dodane odpowiednie dane
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    # Dodatkowe asercje mogą być tutaj umieszczone


@pytest.mark.skip
def test_get_table_rows(api_client):
    url = "/api/table/1/rows"  # Zakładając, że tabela o ID 1 istnieje
    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    # Dodatkowe asercje mogą być tutaj umieszczone
