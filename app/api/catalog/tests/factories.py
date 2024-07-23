import factory
from core.models import Order, OrderItem, Product
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    # See: https://pypi.org/project/factory-boy/
    #  FOr more information about LazyAttributes
    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
    price = factory.LazyAttribute(
        lambda _: fake.pydecimal(left_digits=4, right_digits=2, positive=True)
    )


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=10))
