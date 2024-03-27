# serializers.py
from rest_framework import serializers
from .models import Address, Order, OrderItem, WishlistItem
from shop.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "primary_image", "price", "discounted_price"]

class OrderItemGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity']

class OrderItemSubmissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemGetSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'created', 'updated', 'paid', 'status', 'total_amount',  'items']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = "__all__"


class WishlistGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = WishlistItem
        fields = ["id", "product"]
