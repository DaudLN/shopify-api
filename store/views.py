from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Cart, CartItem, Collection, Customer, Order, Product, ProductImage
from .paginators import ProductPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CartItemSerializer,
    CartSerializer,
    CollectionSerializer,
    CreateCartItemSerializer,
    CustomerSerializer,
    OrderSerilizer,
    ProductImageSerializer,
    ProductSerializer,
    UpdateCartItemSerializer,
)
from .utilities import get_message

# Create your views here.


def home(request):
    return render(request, "home.html")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = (
        Product.objects.prefetch_related("images").select_related("collection").all()
    )

    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    permission_classes = [IsAdminOrReadOnly]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductImageViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=int(self.kwargs["product_pk"]))

    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {"product_id": int(self.kwargs["product_pk"])}


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = (
        Collection.objects.prefetch_related("products")
        .annotate(product_count=Count("products"))
        .all()
    )
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        products_count: int = Product.objects.filter(collection_id=kwargs["pk"]).count()

        if products_count > 0:
            message = get_message("product", products_count)
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=dict(
                    status="fail",
                    detail=message,
                ),
            )
        return super().destroy(request, *args, **kwargs)


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related("items", "items__product").all()


class CartItemViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "option", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCartItemSerializer
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.select_related("product").filter(
            cart_id=self.kwargs["cart_pk"]
        )

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateCartItemSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = CartItemSerializer(instance=instance)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerilizer
    queryset = Order.objects.select_related(
        "customer", "customer__user"
    ).prefetch_related("items", "items__product")


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def me(self, request: Request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = CustomerSerializer(instance=customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
