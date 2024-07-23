from core.models import Product
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets

from .serializers import ProductSerializer


@extend_schema(
    responses={200: ProductSerializer(many=True)},
    description="Retrieve a list of products or a single product. Unauthenticated users have read-only access.",
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
