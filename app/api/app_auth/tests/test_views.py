import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import UserFactory


@pytest.mark.django_db
def test_successful_login(client):
    user = UserFactory.create()
    user.set_password("password123@!")
    user.save()

    user_data = {
        "email": user.email,
        "password": "password123@!",
    }

    response = client.post(reverse("login"), user_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_insuccessful_login_wrong_credentials(client):
    user = UserFactory.create()
    user.set_password("password123@!")
    user.save()

    user_data = {
        "email": user.email,
        "password": "wrongpassword",
    }

    response = client.post(reverse("login"), user_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "access" not in response.data
    assert "refresh" not in response.data


@pytest.mark.django_db
def test_attempted_login_empty_credentials_raises_error(client):
    user_data = {
        # Empty strings simulates a user that tries to login without any details
        "email": "",
        "password": "",
    }

    response = client.post(reverse("login"), user_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "access" not in response.data
    assert "refresh" not in response.data


@pytest.mark.django_db
def test_successful_registration(client):
    user_data = {
        "name": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword@22X",
    }

    response = client.post(reverse("register"), user_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_insuccessful_registration_user_already_exist(client):
    # first we create a user
    existing_user = UserFactory.create(name="testuser", email="testuser@example.com")
    existing_user.set_password("testpassword@22X")
    existing_user.save()

    # and a new user
    user_data = {
        "name": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword@22X",
    }

    response = client.post(reverse("register"), user_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "access" not in response.data
    assert "refresh" not in response.data
