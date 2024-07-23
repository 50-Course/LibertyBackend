# test_product_viewset.py
import pytest
from core.models import Product
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .factories import ProductFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def product():
    return ProductFactory()


@pytest.mark.django_db
def test_list_products_unauthenticated(api_client, product):
    response = api_client.get("/api/products/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_product_unauthenticated(api_client, product):
    response = api_client.get(f"/api/products/{product.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == product.name


@pytest.mark.django_db
def test_create_product_unauthenticated(api_client):
    data = {"name": "New Product", "description": "New Description", "price": 20.0}
    response = api_client.post("/api/products/", data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_product_unauthenticated(api_client, product):
    data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 30.0,
    }
    response = api_client.put(f"/api/products/{product.id}/", data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_product_unauthenticated(api_client, product):
    response = api_client.delete(f"/api/products/{product.id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_product_authenticated(api_client, user):
    api_client.login(username=user.username, password="testpass")
    data = {"name": "New Product", "description": "New Description", "price": 20.0}
    response = api_client.post("/api/products/", data)
    assert response.status_code == status.HTTP_201_CREATED
    api_client.logout()


@pytest.mark.django_db
def test_update_product_authenticated(api_client, user, product):
    api_client.login(username=user.username, password="testpass")
    data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 30.0,
    }
    response = api_client.put(f"/api/products/{product.id}/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Updated Product"
    api_client.logout()


@pytest.mark.django_db
def test_delete_product_authenticated(api_client, user, product):
    api_client.login(username=user.username, password="testpass")
    response = api_client.delete(f"/api/products/{product.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    api_client.logout()
