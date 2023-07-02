from django.urls import include, path
from rest_framework_nested import routers
from .import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename='products')
router.register("collections", views.CollectionViewSet, basename="collections")

product_router = routers.NestedDefaultRouter(
    router, "products", lookup="product")
product_router.register(
    "images", views.ProductImageViewSet, basename="product-images")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(product_router.urls)),
]
