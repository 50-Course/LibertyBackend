from core.models import Order, Product
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderCreateSerializer, OrderSerializer, ProductSerializer


@extend_schema(
    responses={200: ProductSerializer(many=True)},
    description="Retrieve a list of products or a single product. Unauthenticated users have read-only access.",
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(user=self.request.user)
        return super().get_queryset()
