from core.models import Category, Order, OrderItem, Product
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


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Helps to manage order items
    """

    class Meta:
        model = OrderItem
        fields = ["quantity", "product"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer to manage order objects
    """

    items = OrderItemSerializer(source="orderitem_set", many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["user", "items", "date"]
        read_only_fields = ["id"]


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Helps to create objects
    """

    product_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    quantities = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Order
        fields = ["product_ids", "quantities"]

    def create(self, validated_data):
        # retrieve the data we want to use to crete anew order
        user = self.context["request"].user
        products = validated_data.pop("products")
        quantities = validated_data.pop("quantities")

        # create the order
        order = Order.objects.create(user=user)

        # using every product and their quantiy we create a corresponding orderitm
        for product_id, quantity in zip(products, quantities):
            OrderItem.objects.create(
                order=order, product_id=product_id, quantity=quantity
            )
        return order
