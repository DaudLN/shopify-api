from typing import Any
from uuid import uuid4

from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum
from django.utils.text import slugify

# Create your models here.

# Customer managers


class FewProductsInInventory(models.Manager):
    def get_queryset(self):
        return (
            Product.objects.select_related("collection")
            .filter(inventory__lte=5)
            .order_by("-inventory")
        )


class CompletedOrderManager(models.Manager):
    def get_queryset(self):
        return (
            Order.objects.filter(payment_status=Order.PaymentStatus.COMPLETE)
            .prefetch_related("items", "items__product")
            .select_related("customer")
            .annotate(items_count=Count("items"))
        )


class PendingOrderManager(models.Manager):
    def get_queryset(self):
        return (
            Order.objects.filter(payment_status=Order.PaymentStatus.PENDING)
            .prefetch_related("items", "items__product")
            .select_related("customer")
            .annotate(items_count=Count("items"))
        )


class FailOrderManager(models.Manager):
    def get_queryset(self):
        return (
            Order.objects.filter(payment_status=Order.PaymentStatus.FAIL)
            .prefetch_related("items", "items__product")
            .select_related("customer")
            .annotate(items_count=Count("items"))
        )


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discout = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = _("promotion")
        verbose_name_plural = _("promotions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("promotion_detail", kwargs={"pk": self.pk})


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title}"


class Product(models.Model):
    title = models.CharField(max_length=255, db_comment="Product name")
    slug = models.SlugField(_("Slug field"))
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name="products"
    )
    promotions = models.ManyToManyField(
        Promotion, verbose_name=_("promotion"), blank=True
    )
    image = models.ImageField(upload_to="images/products", null=True)

    objects = models.Manager()
    less_in_inventory = FewProductsInInventory()

    class Meta:
        ordering = ["title"]
        managed = True
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(_("Product image"), upload_to="media/images/products")


class Customer(models.Model):
    class Membership(models.TextChoices):
        BLONZE = "B", "Blonze"
        SILVER = "S", "Silver"
        GOLD = "G", "Gold"

    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=Membership.choices, default=Membership.BLONZE
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        permissions = [("view_history", "Can view history")]

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "P", "Pending"
        COMPLETE = "C", "Complete"
        FAIL = "F", "Fail"

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders"
    )

    objects = models.Manager()
    complete = CompletedOrderManager()
    fail = FailOrderManager()
    pending = PendingOrderManager()

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        permissions = [("cancel_order", "Can cancel order")]

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="orderitems"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )


class Cart(models.Model):
    id = models.UUIDField(_("Cart id"), primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Cart_detail", kwargs={"pk": self.pk})

    @property
    def total_price(self):
        return sum([item.total_price for item in self.items.all()])


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = _("CartItem")
        verbose_name_plural = _("CartItems")
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"], name="unique_product_cart"
            ),
        ]

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("CartItem_detail", kwargs={"pk": self.pk})

    @property
    def total_price(self):
        return self.quantity * self.product.unit_price


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresss")

    def __str__(self):
        return f"{self.name} {self.city}"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    name = models.CharField(
        _("Your name"),
        max_length=255,
    )
    description = models.TextField(_("Your review"))
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("Review_detail", kwargs={"pk": self.pk})
