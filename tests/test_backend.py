import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_table(api_client):
    url = "/api/table"
    data = {
        # Tu powinny zostać dodane odpowiednie dane
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    # Dodatkowe asercje mogą być tutaj umieszczone


@pytest.mark.django_db
def test_update_table_structure(api_client):
    url = "/api/table/1"  # Zakładając, że tabela o ID 1 istnieje
    data = {
        # Tu powinny zostać dodane odpowiednie dane
    }
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    # Dodatkowe asercje mogą być tutaj umieszczone


@pytest.mark.django_db
def test_add_table_row(api_client):
    url = "/api/table/1/row"  # Zakładając, że tabela o ID 1 istnieje
    data = {
        # Tu powinny zostać dodane odpowiednie dane
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    # Dodatkowe asercje mogą być tutaj umieszczone


@pytest.mark.django_db
def test_get_table_rows(api_client):
    url = "/api/table/1/rows"  # Zakładając, że tabela o ID 1 istnieje
    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    # Dodatkowe asercje mogą być tutaj umieszczone
