import pytest
from core.models import Product
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def product():
    return ProductFactory()


@pytest.fixture
def products():
    return ProductFactory.create_batch(5)


@pytest.fixture
def auth_client(user):
    client = APIClient()
    token, created = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


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


def test_create_order(auth_client, products):
    url = reverse("order-list")
    product_ids = [product.id for product in products]
    quantities = [1, 2, 3, 4, 5]
    data = {"product_ids": product_ids, "quantities": quantities}
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert Order.objects.first().orderitem_set.count() == 5


def test_get_order_history(auth_client):
    order = OrderFactory(user=auth_client.user)
    OrderItemFactory.create_batch(3, order=order)
    url = reverse("order-list")
    response = auth_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert len(response.data[0]["items"]) == 3


def test_get_product_list(api_client):
    ProductFactory.create_batch(5)
    url = reverse("product-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
