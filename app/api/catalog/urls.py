from rest_framework.routers import DefaultRouter

catalog_router = DefaultRouter(trailing_slash=False)
catalog_router.register(r"products", ProductViewSet, basename="products")

urlpatterns = []

urlpatterns += catalog_router.urls
