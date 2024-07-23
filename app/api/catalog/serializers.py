from core.models import Category, Product
from rest_framework import serializers


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializes the category class of an item in our store

    We are using a seperate serializer here to allow for more
    granular control over the information we want to share
    """

    class Meta:
        model = Category
        fields = ["name"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class for managing Product objects

    """

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ["name", "description", "amount", "category"]
