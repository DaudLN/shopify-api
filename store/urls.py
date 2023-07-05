from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet, basename="collections")
router.register("carts", views.CartViewSet, basename="carts")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")

product_router.register("images", views.ProductImageViewSet, basename="product-images")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(product_router.urls)),
    path(r"", include(cart_router.urls)),
]
