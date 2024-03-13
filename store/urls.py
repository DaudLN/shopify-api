from django.urls import include, path
from rest_framework_nested import routers
from . import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet, basename="collections")
router.register("carts", views.CartViewSet, basename="carts")
router.register("orders", views.OrderViewSet, basename="orders")
router.register("customers", views.CustomerViewSet, basename="customers")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")

product_router.register("images", views.ProductImageViewSet, basename="product-images")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = [
    path(r"", views.home, name="home"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/readoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(r"api/store/", include(router.urls)),
    path(r"api/store/", include(product_router.urls)),
    path(r"api/store/", include(cart_router.urls)),
]
