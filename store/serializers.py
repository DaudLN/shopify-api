from rest_framework import serializers

from .models import Product, Collection, ProductImage


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
        print(validated_data)
        return ProductImage.objects.create(
            product_id=self.context["product_id"], **validated_data
        )


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
        print(validated_data)
        instance.title = validated_data.get("title", instance.title)
        instance.unit_price = validated_data.get("unit_price", 100)
        instance.save()
        return instance
