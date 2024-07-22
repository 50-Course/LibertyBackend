import factory
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("username")
    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("defaultTESTpassword@2024")

        self.save()
