import factory
import Faker
from core.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
