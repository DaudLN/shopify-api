from rest_framework import serializers

from .models import (
    Cart,
    CartItem,
    Customer,
    Order,
    OrderItem,
    Product,
    Collection,
    ProductImage,
)


class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "title", "product_count"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]

    def create(self, validated_data):
        product_id: int = self.context["product_id"]
        return ProductImage.objects.create(product_id=product_id, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    collection = CollectionSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "unit_price",
            "description",
            "collection",
            "images",
        ]

    def update(self, instance: Product, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.unit_price = validated_data.get("unit_price", 100)
        instance.save()
        return instance


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]
        read_only_fields = ["product"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]
        read_only_fields = ["id", "items"]


class CreateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["product_id", "quantity"]

    def validate_product_id(self, value):
        if Product.objects.filter(id=value).exists():
            return value
        raise serializers.ValidationError("Product does not exist")

    def save(self, **kwargs):
        product_id = self.validated_data.get("product_id")
        quantity = self.validated_data.get("quantity")
        cart_id = self.context.get("cart_id")

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class OrderItemSerilizer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "unit_price", "quantity"]


class OrderSerilizer(serializers.ModelSerializer):
    items = OrderItemSerilizer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "placed_at", "payment_status", "items"]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]
