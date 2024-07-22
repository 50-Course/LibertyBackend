"""Create and manage app models and methods."""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

# Create your models here.


class UserManager(BaseUserManager):
    """USER MANAGER CLASS GOING TO MANAGE OUR USER CLASS."""

    def create_user(self, email, password=None, **extra_fields):
        """Create_user method creates and saves new user objects."""
        if not email:
            raise ValueError("User must have valid email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and saves a new super user."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Product(models.Model):
    """
    Item sold at this e-mart

    """

    name = models.CharField(max_length=255)
    description = models.TextField(help_text="Description of the item")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name

    class Meta:
        # Here we want to consider a sceneraio where our store, has thousands
        # or lots of products, and we need to work with large dataset.
        # We might need some form of optimization by tehn.
        #
        # Here we are indexing the name of the product, and the price tag
        # as well as adding, we might also want ot add a UniqueConstriant,
        # A product --> should have a fixed price tag, but that would happen
        # in an ideal world right
        indexes = [
            models.Index(fields=["name", "price"], name="name_price_idx"),
        ]


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Product category, e.g groceries, scents, gadgets",
        db_index=True,
    )  # For product categories, we only want to index the category name to help us in faster data retrieval
    # now in small datasets/querysets, we don't need this optimization, but here just want to drive home a point
    product = models.ForeignKey(
        Product, related_name="product_category", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name
